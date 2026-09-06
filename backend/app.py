from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from auth import auth_bp, role_required
from auth_database import initialize_auth_database

from prediction import predict
from explainability import explain
from lime_explain import lime_explain
from recommendation import recommendation
from report_generator import generate_report

from database import (
    create_table,
    save_prediction,
    get_predictions
)

import os


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(__name__)


# =========================================================
# JWT CONFIGURATION
# =========================================================

app.config["JWT_SECRET_KEY"] = os.environ.get(
    "JWT_SECRET_KEY",
    "development-secret-change-this"
)

jwt = JWTManager(app)


# =========================================================
# CORS
# =========================================================

CORS(app)


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

create_table()
initialize_auth_database()


# =========================================================
# AUTHENTICATION BLUEPRINT
# =========================================================

app.register_blueprint(
    auth_bp,
    url_prefix="/auth"
)


# =========================================================
# FEATURE COUNTS
# =========================================================

EXPECTED_FEATURES = {
    "heart": 13,
    "diabetes": 16,
    "ckd": 24,
    "stroke": 10
}


SUPPORTED_DISEASES = [
    "heart",
    "diabetes",
    "ckd",
    "stroke"
]


# =========================================================
# STROKE FEATURE NAMES
# =========================================================

STROKE_FEATURES = [
    "gender",
    "age",
    "hypertension",
    "heart_disease",
    "ever_married",
    "work_type",
    "Residence_type",
    "avg_glucose_level",
    "bmi",
    "smoking_status"
]


# =========================================================
# BUILD HEART DISEASE PATIENT DATA
# =========================================================

def build_heart_patient_data(data, features):

    return {

        "patient_id":
            data.get("patient_id", ""),

        "patient_name":
            data.get("patient_name", ""),

        "doctor_name":
            data.get("doctor_name", ""),

        "hospital_name":
            data.get("hospital_name", ""),

        "disease":
            "Heart Disease",

        "age":
            features[0],

        "gender":
            "Male" if features[1] == 1 else "Female",

        "cp":
            {
                1: "Typical Angina",
                2: "Atypical Angina",
                3: "Non-anginal Pain",
                4: "Asymptomatic"
            }.get(
                features[2],
                str(features[2])
            ),

        "trestbps":
            features[3],

        "chol":
            features[4],

        "fbs":
            "Yes" if features[5] == 1 else "No",

        "restecg":
            {
                0: "Normal",
                1: "ST-T Wave Abnormality",
                2: "Left Ventricular Hypertrophy"
            }.get(
                features[6],
                str(features[6])
            ),

        "thalach":
            features[7],

        "exang":
            "Yes" if features[8] == 1 else "No",

        "oldpeak":
            features[9],

        "slope":
            {
                1: "Upsloping",
                2: "Flat",
                3: "Downsloping"
            }.get(
                features[10],
                str(features[10])
            ),

        "ca":
            features[11],

        "thal":
            {
                3: "Normal",
                6: "Fixed Defect",
                7: "Reversible Defect"
            }.get(
                features[12],
                str(features[12])
            )
    }


# =========================================================
# BUILD DIABETES PATIENT DATA
# =========================================================

def build_diabetes_patient_data(data, features):

    diabetes_features = [
        "age",
        "gender",
        "polyuria",
        "polydipsia",
        "sudden_weight_loss",
        "weakness",
        "polyphagia",
        "genital_thrush",
        "visual_blurring",
        "itching",
        "irritability",
        "delayed_healing",
        "partial_paresis",
        "muscle_stiffness",
        "alopecia",
        "obesity"
    ]

    patient = {

        "patient_id":
            data.get("patient_id", ""),

        "patient_name":
            data.get("patient_name", ""),

        "doctor_name":
            data.get("doctor_name", ""),

        "hospital_name":
            data.get("hospital_name", ""),

        "disease":
            "Diabetes"
    }

    for index, feature_name in enumerate(
        diabetes_features
    ):

        value = features[index]

        if feature_name == "age":

            patient[feature_name] = value

        elif feature_name == "gender":

            patient[feature_name] = (
                "Male"
                if value == 1
                else "Female"
            )

        else:

            patient[feature_name] = (
                "Yes"
                if value == 1
                else "No"
            )

    return patient


# =========================================================
# BUILD CKD PATIENT DATA
# =========================================================

def build_ckd_patient_data(data, features):

    ckd_features = [

        "age",
        "bp",
        "sg",
        "al",
        "su",
        "rbc",
        "pc",
        "pcc",
        "ba",
        "bgr",
        "bu",
        "sc",
        "sod",
        "pot",
        "hemo",
        "pcv",
        "wbcc",
        "rbcc",
        "htn",
        "dm",
        "cad",
        "appet",
        "pe",
        "ane"

    ]

    patient = {

        "patient_id":
            data.get("patient_id", ""),

        "patient_name":
            data.get("patient_name", ""),

        "doctor_name":
            data.get("doctor_name", ""),

        "hospital_name":
            data.get("hospital_name", ""),

        "disease":
            "Chronic Kidney Disease"
    }

    numeric_features = [

        "age",
        "bp",
        "sg",
        "al",
        "su",
        "bgr",
        "bu",
        "sc",
        "sod",
        "pot",
        "hemo",
        "pcv",
        "wbcc",
        "rbcc"

    ]

    yes_no_features = [

        "rbc",
        "pc",
        "pcc",
        "ba",
        "htn",
        "dm",
        "cad",
        "pe",
        "ane"

    ]

    for index, feature_name in enumerate(
        ckd_features
    ):

        value = features[index]

        if feature_name in numeric_features:

            patient[feature_name] = value

        elif feature_name in yes_no_features:

            patient[feature_name] = (
                "Yes"
                if value == 1
                else "No"
            )

        elif feature_name == "appet":

            patient[feature_name] = (
                "Poor"
                if value == 1
                else "Good"
            )

    return patient


# =========================================================
# BUILD STROKE PATIENT DATA
# =========================================================

def build_stroke_patient_data(data, features):

    patient = {

        "patient_id":
            data.get("patient_id", ""),

        "patient_name":
            data.get("patient_name", ""),

        "doctor_name":
            data.get("doctor_name", ""),

        "hospital_name":
            data.get("hospital_name", ""),

        "disease":
            "Stroke"
    }

    # -----------------------------------------------------
    # Frontend may send Stroke features as a dictionary
    # -----------------------------------------------------

    if isinstance(features, dict):

        for feature_name in STROKE_FEATURES:

            if feature_name not in features:

                raise ValueError(
                    f"Missing stroke feature: {feature_name}"
                )

            patient[feature_name] = features[
                feature_name
            ]

        return patient

    # -----------------------------------------------------
    # Or frontend may send them as a list
    # -----------------------------------------------------

    if isinstance(features, (list, tuple)):

        if len(features) != len(STROKE_FEATURES):

            raise ValueError(
                "Stroke requires "
                f"{len(STROKE_FEATURES)} features."
            )

        for index, feature_name in enumerate(
            STROKE_FEATURES
        ):

            patient[feature_name] = features[index]

        return patient

    raise ValueError(
        "Stroke features must be provided "
        "as a dictionary or list."
    )


# =========================================================
# BUILD PATIENT DATA
# =========================================================

def build_patient_data(data, features, disease):

    if disease == "heart":

        return build_heart_patient_data(
            data,
            features
        )

    if disease == "diabetes":

        return build_diabetes_patient_data(
            data,
            features
        )

    if disease == "ckd":

        return build_ckd_patient_data(
            data,
            features
        )

    if disease == "stroke":

        return build_stroke_patient_data(
            data,
            features
        )

    raise ValueError(
        f"Unsupported disease: {disease}"
    )


# =========================================================
# RECOMMENDATION HANDLER
# =========================================================

def get_recommendation(
    prediction_class,
    probability,
    disease
):

    # -----------------------------------------------------
    # Existing recommendation.py handles:
    # heart / diabetes / ckd
    # -----------------------------------------------------

    if disease != "stroke":

        return recommendation(
            prediction_class,
            probability,
            disease
        )

    # -----------------------------------------------------
    # Stroke recommendation
    # -----------------------------------------------------

    if prediction_class == 1:

        return {

            "risk": "High",

            "recommendation":
                "The model indicates a higher likelihood "
                "of stroke risk. Prompt consultation with "
                "a healthcare professional is strongly "
                "recommended for further clinical "
                "evaluation and appropriate diagnostic "
                "assessment."

        }

    return {

        "risk": "Low",

        "recommendation":
            "The model indicates a lower likelihood "
            "of stroke risk. This result should still "
            "be interpreted together with clinical "
            "assessment and professional judgement."

    }


# =========================================================
# LIME HANDLER
# =========================================================

def get_lime_explanation(
    features,
    disease
):

    if disease == "stroke":

        return []

    try:

        return lime_explain(
            features,
            disease
        )

    except Exception as error:

        print(
            "LIME explanation error:",
            error
        )

        return []


# =========================================================
# HOME / HEALTH CHECK
# =========================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({

        "project":
            "Explainable AI Clinical Decision Support System",

        "status":
            "Running",

        "supported_diseases":
            SUPPORTED_DISEASES,

        "version":
            "3.0"

    })


# =========================================================
# PREDICTION
#
# Accessible to:
# admin
# doctor
# staff
# =========================================================

@app.route(
    "/predict",
    methods=["POST"]
)
@role_required(
    "doctor",
    "staff"
)
def prediction():

    try:

        data = request.get_json()

        if not data:

            return jsonify({

                "success": False,

                "error":
                    "Invalid JSON data."

            }), 400

        disease = data.get(
            "disease",
            "heart"
        ).lower()

        # -------------------------------------------------
        # Validate disease
        # -------------------------------------------------

        if disease not in SUPPORTED_DISEASES:

            return jsonify({

                "success": False,

                "error":
                    "Unsupported disease. "
                    "Use heart, diabetes, ckd, or stroke."

            }), 400

        # -------------------------------------------------
        # Validate features
        # -------------------------------------------------

        if "features" not in data:

            return jsonify({

                "success": False,

                "error":
                    "Missing 'features' field."

            }), 400

        features = data["features"]

        # -------------------------------------------------
        # Stroke can use dictionary or list
        # -------------------------------------------------

        if disease == "stroke" and isinstance(
            features,
            dict
        ):

            missing_features = [

                feature

                for feature in STROKE_FEATURES

                if feature not in features

            ]

            if missing_features:

                return jsonify({

                    "success": False,

                    "error":
                        "Missing stroke features: "
                        + ", ".join(missing_features)

                }), 400

        else:

            if not isinstance(
                features,
                (list, tuple)
            ):

                return jsonify({

                    "success": False,

                    "error":
                        "Features must be provided "
                        "as a list."

                }), 400

            if len(features) != EXPECTED_FEATURES[disease]:

                return jsonify({

                    "success": False,

                    "error":
                        f"{disease} requires "
                        f"{EXPECTED_FEATURES[disease]} "
                        "features."

                }), 400

        # -------------------------------------------------
        # MODEL PREDICTION
        # -------------------------------------------------

        result = predict(
            features,
            disease
        )

        # -------------------------------------------------
        # SHAP
        # -------------------------------------------------

        explanation = explain(
            features,
            disease
        )

        # -------------------------------------------------
        # LIME
        # -------------------------------------------------

        lime = get_lime_explanation(
            features,
            disease
        )

        # -------------------------------------------------
        # RECOMMENDATION
        # -------------------------------------------------

        advice = get_recommendation(

            result["prediction_class"],

            result["probability"],

            disease

        )

        result["risk_level"] = advice["risk"]

        result["recommendation"] = (
            advice["recommendation"]
        )

        result["top_features"] = explanation

        result["lime_features"] = lime

        # -------------------------------------------------
        # PATIENT INFORMATION
        # -------------------------------------------------

        patient = build_patient_data(

            data,

            features,

            disease

        )

        # -------------------------------------------------
        # SAVE HISTORY
        # -------------------------------------------------

        save_prediction(

            patient,

            result

        )

        return jsonify(result), 200

    except Exception as error:

        print(
            "Prediction Error:",
            error
        )

        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500


# =========================================================
# CLINICAL PDF REPORT
#
# Accessible to:
# admin
# doctor
# staff
# =========================================================

@app.route(
    "/report",
    methods=["POST"]
)
@role_required(
    "admin",
    "doctor",
    "staff"
)
def report():

    try:

        data = request.get_json()

        print(
            "Received from frontend:",
            data
        )

        if not data:

            return jsonify({

                "success": False,

                "error":
                    "Invalid JSON data."

            }), 400

        disease = data.get(
            "disease",
            "heart"
        ).lower()

        # -------------------------------------------------
        # Validate disease
        # -------------------------------------------------

        if disease not in SUPPORTED_DISEASES:

            return jsonify({

                "success": False,

                "error":
                    "Unsupported disease."

            }), 400

        # -------------------------------------------------
        # Validate features
        # -------------------------------------------------

        if "features" not in data:

            return jsonify({

                "success": False,

                "error":
                    "Missing 'features' field."

            }), 400

        features = data["features"]

        if disease == "stroke" and isinstance(
            features,
            dict
        ):

            missing_features = [

                feature

                for feature in STROKE_FEATURES

                if feature not in features

            ]

            if missing_features:

                return jsonify({

                    "success": False,

                    "error":
                        "Missing stroke features: "
                        + ", ".join(missing_features)

                }), 400

        else:

            if not isinstance(
                features,
                (list, tuple)
            ):

                return jsonify({

                    "success": False,

                    "error":
                        "Features must be provided "
                        "as a list."

                }), 400

            if len(features) != EXPECTED_FEATURES[disease]:

                return jsonify({

                    "success": False,

                    "error":
                        f"{disease} requires "
                        f"{EXPECTED_FEATURES[disease]} "
                        "features."

                }), 400

        # -------------------------------------------------
        # MODEL PREDICTION
        # -------------------------------------------------

        result = predict(
            features,
            disease
        )

        # -------------------------------------------------
        # SHAP
        # -------------------------------------------------

        explanation = explain(
            features,
            disease
        )

        # -------------------------------------------------
        # LIME
        # -------------------------------------------------

        if (
            "lime_features" in data
            and data["lime_features"]
        ):

            lime = data["lime_features"]

            print(
                "Using LIME explanation "
                "received from frontend."
            )

        else:

            lime = get_lime_explanation(
                features,
                disease
            )

            if disease == "stroke":

                print(
                    "Stroke LIME is not available "
                    "from current backend lime_explain.py."
                )

        # -------------------------------------------------
        # RECOMMENDATION
        # -------------------------------------------------

        advice = get_recommendation(

            result["prediction_class"],

            result["probability"],

            disease

        )

        result["risk_level"] = advice["risk"]

        result["recommendation"] = (
            advice["recommendation"]
        )

        result["top_features"] = explanation

        result["lime_features"] = lime

        # -------------------------------------------------
        # PATIENT DATA
        # -------------------------------------------------

        patient = build_patient_data(

            data,

            features,

            disease

        )

        # -------------------------------------------------
        # REPORT DIRECTORY
        # -------------------------------------------------

        reports_dir = os.path.join(

            os.path.dirname(
                os.path.abspath(__file__)
            ),

            "reports"

        )

        os.makedirs(

            reports_dir,

            exist_ok=True

        )

        output_path = os.path.join(

            reports_dir,

            "clinical_report.pdf"

        )

        # -------------------------------------------------
        # GENERATE PDF
        # -------------------------------------------------

        generate_report(

            patient,

            result,

            output_path

        )

        return send_file(

            output_path,

            as_attachment=True,

            download_name=
                "Clinical_Report.pdf"

        )

    except Exception as error:

        print(
            "Report Error:",
            error
        )

        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500

# =========================================================
# DASHBOARD STATISTICS
# =========================================================

@app.route(
    "/stats",
    methods=["GET"]
)
@role_required(
    "doctor",
    "staff"
)
def statistics():

    try:

        history_data = get_predictions()

        total_cases = len(history_data)

        high_risk = sum(
            1
            for item in history_data
            if str(item.get("risk_level", "")).lower() == "high"
        )

        low_risk = sum(
            1
            for item in history_data
            if str(item.get("risk_level", "")).lower() == "low"
        )

        return jsonify({

            "success": True,

            "cases_processed": total_cases,

            "high_risk_flags": high_risk,

            "low_risk_cases": low_risk

        }), 200

    except Exception as error:

        print(
            "Statistics Error:",
            error
        )

        return jsonify({

            "success": False,

            "error": str(error)

        }), 500
# =========================================================
# HISTORY
#
# Accessible only to:
# doctor
# =========================================================

@app.route(
    "/history",
    methods=["GET"]
)
@role_required(
    "doctor"
)
def history():

    try:

        history_data = get_predictions()

        return jsonify(
            history_data
        ), 200

    except Exception as error:

        print(
            "History Error:",
            error
        )

        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    port = int(

        os.environ.get(
            "PORT",
            5000
        )

    )

    app.run(

        host="0.0.0.0",

        port=port,

        debug=True

    )