from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

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


# ==========================================
# Flask Application
# ==========================================

app = Flask(__name__)

CORS(app)

create_table()


# ==========================================
# Build Heart Disease Patient Data
# ==========================================

def build_heart_patient_data(data, features):

    return {

        "patient_id": data.get("patient_id", ""),

        "patient_name": data.get("patient_name", ""),

        "doctor_name": data.get("doctor_name", ""),

        "hospital_name": data.get("hospital_name", ""),

        "disease": "Heart Disease",

        "age": features[0],

        "gender":
            "Male" if features[1] == 1 else "Female",

        "cp": {
            1: "Typical Angina",
            2: "Atypical Angina",
            3: "Non-anginal Pain",
            4: "Asymptomatic"
        }.get(
            features[2],
            str(features[2])
        ),

        "trestbps": features[3],

        "chol": features[4],

        "fbs":
            "Yes" if features[5] == 1 else "No",

        "restecg": {
            0: "Normal",
            1: "ST-T Wave Abnormality",
            2: "Left Ventricular Hypertrophy"
        }.get(
            features[6],
            str(features[6])
        ),

        "thalach": features[7],

        "exang":
            "Yes" if features[8] == 1 else "No",

        "oldpeak": features[9],

        "slope": {
            1: "Upsloping",
            2: "Flat",
            3: "Downsloping"
        }.get(
            features[10],
            str(features[10])
        ),

        "ca": features[11],

        "thal": {
            3: "Normal",
            6: "Fixed Defect",
            7: "Reversible Defect"
        }.get(
            features[12],
            str(features[12])
        )
    }


# ==========================================
# Build Diabetes Patient Data
# ==========================================

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

    # ======================================
    # Convert Diabetes Features
    # ======================================

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


# ==========================================
# Build CKD Patient Data
# ==========================================

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

    # ======================================
    # CKD Feature Conversion
    # ======================================

    for index, feature_name in enumerate(
        ckd_features
    ):

        value = features[index]

        # Numeric features
        if feature_name in [
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
        ]:

            patient[feature_name] = value

        # Binary categorical features
        elif feature_name in [
            "rbc",
            "pc",
            "pcc",
            "ba",
            "htn",
            "dm",
            "cad",
            "pe",
            "ane"
        ]:

            patient[feature_name] = (
                "Yes"
                if value == 1
                else "No"
            )

        # Appetite
        elif feature_name == "appet":

            patient[feature_name] = (
                "Poor"
                if value == 1
                else "Good"
            )

    return patient


# ==========================================
# Build Patient Data
# ==========================================

def build_patient_data(data, features, disease):

    if disease == "diabetes":

        return build_diabetes_patient_data(
            data,
            features
        )

    elif disease == "ckd":

        return build_ckd_patient_data(
            data,
            features
        )

    return build_heart_patient_data(
        data,
        features
    )


# ==========================================
# Home
# ==========================================

@app.route("/")
def home():

    return jsonify({

        "project":
            "Explainable AI Clinical Decision Support System",

        "status":
            "Running",

        "version":
            "3.0",

        "supported_diseases": [

            "heart",

            "diabetes",

            "ckd"

        ]

    })


# ==========================================
# Prediction
# ==========================================

@app.route("/predict", methods=["POST"])
def prediction():

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "Invalid JSON data"
        }), 400


    # ======================================
    # Disease
    # ======================================

    disease = data.get(
        "disease",
        "heart"
    ).lower()


    if disease not in [
        "heart",
        "diabetes",
        "ckd"
    ]:

        return jsonify({

            "error":
                "Unsupported disease. Use 'heart', 'diabetes', or 'ckd'."

        }), 400


    # ======================================
    # Features
    # ======================================

    if "features" not in data:

        return jsonify({

            "error":
                "Missing 'features' field"

        }), 400


    features = data["features"]


    # ======================================
    # Validate Feature Count
    # ======================================

    expected_features = {

        "heart": 13,

        "diabetes": 16,

        "ckd": 24

    }


    if len(features) != expected_features[disease]:

        return jsonify({

            "error":
                f"{disease} requires "
                f"{expected_features[disease]} features."

        }), 400


    # ======================================
    # Prediction
    # ======================================

    result = predict(
        features,
        disease
    )


    # ======================================
    # SHAP
    # ======================================

    explanation = explain(
        features,
        disease
    )


    # ======================================
    # LIME
    # ======================================

    lime = lime_explain(
        features,
        disease
    )


    # ======================================
    # Recommendation
    # ======================================

    advice = recommendation(

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


    # ======================================
    # Patient Information
    # ======================================

    patient = build_patient_data(

        data,

        features,

        disease

    )


    # ======================================
    # Save History
    # ======================================

    save_prediction(

        patient,

        result

    )


    return jsonify(result)


# ==========================================
# Generate Clinical Report
# ==========================================

@app.route("/report", methods=["POST"])
def report():

    data = request.get_json()

    print(
        "Received from frontend:",
        data
    )


    if not data:

        return jsonify({

            "error":
                "Invalid JSON data"

        }), 400


    # ======================================
    # Disease
    # ======================================

    disease = data.get(
        "disease",
        "heart"
    ).lower()


    if disease not in [
        "heart",
        "diabetes",
        "ckd"
    ]:

        return jsonify({

            "error":
                "Unsupported disease"

        }), 400


    # ======================================
    # Features
    # ======================================

    if "features" not in data:

        return jsonify({

            "error":
                "Missing 'features' field"

        }), 400


    features = data["features"]


    expected_features = {

        "heart": 13,

        "diabetes": 16,

        "ckd": 24

    }


    if len(features) != expected_features[disease]:

        return jsonify({

            "error":
                f"{disease} requires "
                f"{expected_features[disease]} features."

        }), 400


    # ======================================
    # Prediction
    # ======================================

    result = predict(

        features,

        disease

    )


    # ======================================
    # SHAP
    # ======================================

    explanation = explain(

        features,

        disease

    )


    # ======================================
    # LIME
    # ======================================

    lime = lime_explain(

        features,

        disease

    )


    # ======================================
    # Recommendation
    # ======================================

    advice = recommendation(

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


    # ======================================
    # Patient
    # ======================================

    patient = build_patient_data(

        data,

        features,

        disease

    )


    # ======================================
    # Report Directory
    # ======================================

    reports_dir = os.path.join(

        os.path.dirname(__file__),

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


    # ======================================
    # Generate PDF
    # ======================================

    generate_report(

        patient,

        result,

        output_path

    )


    return send_file(

        output_path,

        as_attachment=True,

        download_name="Clinical_Report.pdf"

    )


# ==========================================
# Prediction History
# ==========================================

@app.route("/history", methods=["GET"])
def history():

    history_data = get_predictions()

    return jsonify(history_data)


# ==========================================
# Run Application
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )