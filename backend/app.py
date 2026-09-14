from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from auth import auth_bp, role_required

from auth_database import (
    initialize_auth_database,
    create_bootstrap_admin
)

from prediction import predict
from explainability import explain
from lime_explain import lime_explain
from recommendation import recommendation
from report_generator import generate_report

from shap_lime_agreement import (
    calculate_shap_lime_agreement
)

from database import (
    create_table,
    save_prediction,
    get_predictions
)

import os
import copy
import itertools


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {"origins": "https://clinical-cdss-frontend.onrender.com"}},
    supports_credentials=True
)

# =========================================================
# JWT CONFIGURATION
# =========================================================

app.config["JWT_SECRET_KEY"] = os.environ.get(
    "JWT_SECRET_KEY",
    "development-secret-change-this-key-2026"
)

jwt = JWTManager(app)

# =========================================================
# DATABASE INITIALIZATION
# =========================================================

create_table()

initialize_auth_database()

create_bootstrap_admin()


# =========================================================
# AUTHENTICATION BLUEPRINT
# =========================================================

app.register_blueprint(
    auth_bp,
    url_prefix="/auth"
)


# =========================================================
# DISEASE CONFIGURATION
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
# DISEASE DISPLAY NAMES
# =========================================================

DISEASE_DISPLAY_NAMES = {
    "heart": "Heart Disease",
    "diabetes": "Diabetes",
    "ckd": "Chronic Kidney Disease",
    "stroke": "Stroke"
}


# =========================================================
# FEATURE NAMES
# =========================================================

HEART_FEATURES = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal"
]


DIABETES_FEATURES = [
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


CKD_FEATURES = [
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


FEATURE_NAMES = {
    "heart": HEART_FEATURES,
    "diabetes": DIABETES_FEATURES,
    "ckd": CKD_FEATURES,
    "stroke": STROKE_FEATURES
}


# =========================================================
# HUMAN READABLE FEATURE NAMES
# =========================================================

FEATURE_LABELS = {

    "age": "Age",
    "sex": "Gender",
    "gender": "Gender",

    "cp": "Chest Pain Type",
    "trestbps": "Resting Blood Pressure",
    "chol": "Serum Cholesterol",
    "fbs": "Fasting Blood Sugar",
    "restecg": "Resting ECG",
    "thalach": "Maximum Heart Rate",
    "exang": "Exercise Induced Angina",
    "oldpeak": "ST Depression",
    "slope": "ST Segment Slope",
    "ca": "Major Vessels",
    "thal": "Thalassemia",

    "polyuria": "Polyuria",
    "polydipsia": "Polydipsia",
    "sudden_weight_loss": "Sudden Weight Loss",
    "weakness": "Weakness",
    "polyphagia": "Polyphagia",
    "genital_thrush": "Genital Thrush",
    "visual_blurring": "Visual Blurring",
    "itching": "Itching",
    "irritability": "Irritability",
    "delayed_healing": "Delayed Healing",
    "partial_paresis": "Partial Paresis",
    "muscle_stiffness": "Muscle Stiffness",
    "alopecia": "Alopecia",
    "obesity": "Obesity",

    "bp": "Blood Pressure",
    "sg": "Specific Gravity",
    "al": "Albumin",
    "su": "Sugar",
    "rbc": "Red Blood Cells",
    "pc": "Pus Cell",
    "pcc": "Pus Cell Clumps",
    "ba": "Bacteria",
    "bgr": "Blood Glucose",
    "bu": "Blood Urea",
    "sc": "Serum Creatinine",
    "sod": "Sodium",
    "pot": "Potassium",
    "hemo": "Hemoglobin",
    "pcv": "Packed Cell Volume",
    "wbcc": "White Blood Cell Count",
    "rbcc": "Red Blood Cell Count",
    "htn": "Hypertension",
    "dm": "Diabetes Mellitus",
    "cad": "Coronary Artery Disease",
    "appet": "Appetite",
    "pe": "Pedal Edema",
    "ane": "Anemia",

    "hypertension": "Hypertension",
    "heart_disease": "Heart Disease",
    "ever_married": "Ever Married",
    "work_type": "Work Type",
    "Residence_type": "Residence Type",
    "avg_glucose_level": "Average Glucose Level",
    "bmi": "Body Mass Index",
    "smoking_status": "Smoking Status"
}


# =========================================================
# COUNTERFACTUAL TARGET
# =========================================================

def opposite_class(prediction_class):
    return 0 if int(prediction_class) == 1 else 1


# =========================================================
# NORMALIZE DISEASE
# =========================================================

def normalize_disease(disease):

    if disease is None:
        return "heart"

    value = str(disease).strip().lower()

    aliases = {
        "heart": "heart",
        "heart disease": "heart",
        "heart_disease": "heart",

        "diabetes": "diabetes",
        "diabetic": "diabetes",

        "ckd": "ckd",
        "kidney": "ckd",
        "kidney disease": "ckd",
        "chronic kidney disease": "ckd",
        "chronic_kidney_disease": "ckd",

        "stroke": "stroke"
    }

    return aliases.get(value, value)


# =========================================================
# FEATURE NAME
# =========================================================

def feature_label(feature):

    return FEATURE_LABELS.get(
        feature,
        str(feature).replace("_", " ").title()
    )


# =========================================================
# SAFE NUMERIC
# =========================================================

def safe_float(value, default=0.0):

    try:
        return float(value)
    except Exception:
        return float(default)


# =========================================================
# SAFE INTEGER
# =========================================================

def safe_int(value, default=0):

    try:
        return int(float(value))
    except Exception:
        return int(default)


# =========================================================
# BUILD HEART PATIENT DATA
# =========================================================

def build_heart_patient_data(data, features):

    if not isinstance(features, (list, tuple)):
        raise ValueError(
            "Heart Disease features must be a list."
        )

    if len(features) != 13:
        raise ValueError(
            "Heart Disease requires 13 features."
        )

    return {

        "patient_id": data.get(
            "patient_id",
            ""
        ),

        "patient_name": data.get(
            "patient_name",
            ""
        ),

        "doctor_name": data.get(
            "doctor_name",
            ""
        ),

        "hospital_name": data.get(
            "hospital_name",
            ""
        ),

        "disease":
            "Heart Disease",

        "age":
            features[0],

        "gender":
            "Male"
            if safe_int(features[1]) == 1
            else "Female",

        "cp":
            {
                1: "Typical Angina",
                2: "Atypical Angina",
                3: "Non-anginal Pain",
                4: "Asymptomatic"
            }.get(
                safe_int(features[2]),
                str(features[2])
            ),

        "trestbps":
            features[3],

        "chol":
            features[4],

        "fbs":
            "Yes"
            if safe_int(features[5]) == 1
            else "No",

        "restecg":
            {
                0: "Normal",
                1: "ST-T Wave Abnormality",
                2: "Left Ventricular Hypertrophy"
            }.get(
                safe_int(features[6]),
                str(features[6])
            ),

        "thalach":
            features[7],

        "exang":
            "Yes"
            if safe_int(features[8]) == 1
            else "No",

        "oldpeak":
            features[9],

        "slope":
            {
                0: "Upsloping",
                1: "Flat",
                2: "Downsloping",
                3: "Downsloping"
            }.get(
                safe_int(features[10]),
                str(features[10])
            ),

        "ca":
            features[11],

        "thal":
            {
                0: "Normal",
                1: "Fixed Defect",
                2: "Reversible Defect",
                3: "Other"
            }.get(
                safe_int(features[12]),
                str(features[12])
            )
    }


# =========================================================
# BUILD DIABETES PATIENT DATA
# =========================================================

def build_diabetes_patient_data(data, features):

    if not isinstance(features, (list, tuple)):
        raise ValueError(
            "Diabetes features must be a list."
        )

    if len(features) != 16:
        raise ValueError(
            "Diabetes requires 16 features."
        )

    def yes_no(value):

        return (
            "Yes"
            if safe_int(value) == 1
            else "No"
        )

    return {

        "patient_id": data.get(
            "patient_id",
            ""
        ),

        "patient_name": data.get(
            "patient_name",
            ""
        ),

        "doctor_name": data.get(
            "doctor_name",
            ""
        ),

        "hospital_name": data.get(
            "hospital_name",
            ""
        ),

        "disease":
            "Diabetes",

        "age":
            features[0],

        "gender":
            "Male"
            if safe_int(features[1]) == 1
            else "Female",

        "polyuria":
            yes_no(features[2]),

        "polydipsia":
            yes_no(features[3]),

        "sudden_weight_loss":
            yes_no(features[4]),

        "weakness":
            yes_no(features[5]),

        "polyphagia":
            yes_no(features[6]),

        "genital_thrush":
            yes_no(features[7]),

        "visual_blurring":
            yes_no(features[8]),

        "itching":
            yes_no(features[9]),

        "irritability":
            yes_no(features[10]),

        "delayed_healing":
            yes_no(features[11]),

        "partial_paresis":
            yes_no(features[12]),

        "muscle_stiffness":
            yes_no(features[13]),

        "alopecia":
            yes_no(features[14]),

        "obesity":
            yes_no(features[15])
    }


# =========================================================
# BUILD CKD PATIENT DATA
# =========================================================

def build_ckd_patient_data(data, features):

    if not isinstance(features, (list, tuple)):
        raise ValueError(
            "CKD features must be a list."
        )

    if len(features) != 24:
        raise ValueError(
            "CKD requires 24 features."
        )

    def yes_no(value):

        return (
            "Yes"
            if safe_int(value) == 1
            else "No"
        )

    return {

        "patient_id": data.get(
            "patient_id",
            ""
        ),

        "patient_name": data.get(
            "patient_name",
            ""
        ),

        "doctor_name": data.get(
            "doctor_name",
            ""
        ),

        "hospital_name": data.get(
            "hospital_name",
            ""
        ),

        "disease":
            "Chronic Kidney Disease",

        "age":
            features[0],

        "bp":
            features[1],

        "sg":
            features[2],

        "al":
            features[3],

        "su":
            features[4],

        "rbc":
            features[5],

        "pc":
            features[6],

        "pcc":
            features[7],

        "ba":
            features[8],

        "bgr":
            features[9],

        "bu":
            features[10],

        "sc":
            features[11],

        "sod":
            features[12],

        "pot":
            features[13],

        "hemo":
            features[14],

        "pcv":
            features[15],

        "wbcc":
            features[16],

        "rbcc":
            features[17],

        "htn":
            yes_no(features[18]),

        "dm":
            yes_no(features[19]),

        "cad":
            yes_no(features[20]),

        "appet":
            features[21],

        "pe":
            yes_no(features[22]),

        "ane":
            yes_no(features[23])
    }


# =========================================================
# BUILD STROKE PATIENT DATA
# =========================================================

def build_stroke_patient_data(data, features):

    patient = {

        "patient_id": data.get(
            "patient_id",
            ""
        ),

        "patient_name": data.get(
            "patient_name",
            ""
        ),

        "doctor_name": data.get(
            "doctor_name",
            ""
        ),

        "hospital_name": data.get(
            "hospital_name",
            ""
        ),

        "disease":
            "Stroke"
    }

    if isinstance(features, dict):

        for feature_name in STROKE_FEATURES:

            if feature_name in features:

                patient[
                    feature_name
                ] = features[
                    feature_name
                ]

            elif (
                feature_name == "Residence_type"
                and
                "residence_type" in features
            ):

                patient[
                    feature_name
                ] = features[
                    "residence_type"
                ]

            else:

                raise ValueError(
                    "Missing stroke feature: "
                    + feature_name
                )

        return patient

    if isinstance(features, (list, tuple)):

        if len(features) != 10:
            raise ValueError(
                "Stroke requires 10 features."
            )

        for index, feature_name in enumerate(
            STROKE_FEATURES
        ):

            patient[
                feature_name
            ] = features[index]

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
        "Unsupported disease: "
        + str(disease)
    )


# =========================================================
# VALIDATE FEATURES
# =========================================================

def validate_features(features, disease):

    if disease not in SUPPORTED_DISEASES:

        raise ValueError(
            "Unsupported disease."
        )

    if disease == "stroke":

        if isinstance(features, dict):

            missing = []

            for feature in STROKE_FEATURES:

                if feature in features:
                    continue

                if (
                    feature == "Residence_type"
                    and
                    "residence_type" in features
                ):
                    continue

                missing.append(feature)

            if missing:

                raise ValueError(
                    "Missing stroke features: "
                    + ", ".join(missing)
                )

            return

        if isinstance(features, (list, tuple)):

            if len(features) != 10:

                raise ValueError(
                    "Stroke requires 10 features."
                )

            return

        raise ValueError(
            "Stroke features must be a dictionary or list."
        )

    if not isinstance(features, (list, tuple)):

        raise ValueError(
            disease
            + " features must be provided as a list."
        )

    expected = EXPECTED_FEATURES[disease]

    if len(features) != expected:

        raise ValueError(
            disease
            + " requires "
            + str(expected)
            + " features."
        )


# =========================================================
# STROKE DICT -> VECTOR
# =========================================================

def stroke_dict_to_vector(features):

    if not isinstance(features, dict):

        return list(features)

    result = dict(features)

    if (
        "Residence_type" not in result
        and
        "residence_type" in result
    ):

        result["Residence_type"] = result[
            "residence_type"
        ]

    return [
        result[name]
        for name in STROKE_FEATURES
    ]


# =========================================================
# COUNTERFACTUAL INPUT
# =========================================================

def prepare_counterfactual_input(features, disease):

    if disease == "stroke":

        if isinstance(features, dict):

            result = dict(features)

            if (
                "Residence_type" not in result
                and
                "residence_type" in result
            ):

                result["Residence_type"] = result[
                    "residence_type"
                ]

            return result

        return {
            name: features[index]
            for index, name in enumerate(
                STROKE_FEATURES
            )
        }

    if isinstance(features, dict):

        return dict(features)

    names = FEATURE_NAMES[disease]

    return {
        names[index]: features[index]
        for index in range(
            len(names)
        )
    }


# =========================================================
# COUNTERFACTUAL HEART IMPORT
# =========================================================

def load_heart_counterfactual_module():

    try:

        import counterfactual_heart

        return counterfactual_heart

    except Exception as error:

        print(
            "Heart counterfactual module unavailable:",
            repr(error)
        )

        return None


# =========================================================
# HEART COUNTERFACTUAL
# =========================================================

def run_heart_counterfactual(
    features,
    max_results=5
):

    module = load_heart_counterfactual_module()

    if module is None:

        return []

    try:

        if hasattr(
            module,
            "build_feature_dict"
        ):

            original = module.build_feature_dict(
                features,
                "heart"
            )

        else:

            original = prepare_counterfactual_input(
                features,
                "heart"
            )

        function = getattr(
            module,
            "find_counterfactuals",
            None
        )

        if function is None:

            return []

        try:

            result = function(
                original,
                max_results=max_results
            )

        except TypeError:

            result = function(
                original
            )

        if isinstance(result, tuple):

            if len(result) >= 3:

                return result[2] or []

            if len(result) == 1:

                return result[0] or []

        return result or []

    except Exception as error:

        print(
            "Heart counterfactual error:",
            repr(error)
        )

        return []


# =========================================================
# GENERIC COUNTERFACTUAL CANDIDATES
# =========================================================

def candidate_values(
    disease,
    feature,
    original
):

    value = original

    # -----------------------------------------------------
    # HEART
    # -----------------------------------------------------

    if disease == "heart":

        grids = {

            "age": [
                max(18, safe_int(value) - 10),
                max(18, safe_int(value) - 5),
                safe_int(value) + 5,
                safe_int(value) + 10
            ],

            "sex": [0, 1],

            "cp": [1, 2, 3, 4],

            "trestbps": [
                max(80, safe_int(value) - 20),
                max(80, safe_int(value) - 10),
                safe_int(value) + 10,
                safe_int(value) + 20
            ],

            "chol": [
                max(100, safe_int(value) - 40),
                max(100, safe_int(value) - 20),
                safe_int(value) + 20,
                safe_int(value) + 40
            ],

            "fbs": [0, 1],

            "restecg": [0, 1, 2],

            "thalach": [
                max(60, safe_int(value) - 30),
                max(60, safe_int(value) - 15),
                safe_int(value) + 15,
                safe_int(value) + 30
            ],

            "exang": [0, 1],

            "oldpeak": [
                0.0,
                0.5,
                1.0,
                2.0,
                3.0
            ],

            "slope": [0, 1, 2],

            "ca": [0, 1, 2, 3],

            "thal": [0, 1, 2, 3]
        }

        return grids.get(
            feature,
            [value]
        )

    # -----------------------------------------------------
    # DIABETES
    # -----------------------------------------------------

    if disease == "diabetes":

        binary_features = {
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
        }

        if feature in binary_features:

            return [0, 1]

        if feature == "gender":

            return [0, 1]

        if feature == "age":

            return [
                max(1, safe_int(value) - 10),
                max(1, safe_int(value) - 5),
                safe_int(value) + 5,
                safe_int(value) + 10
            ]

    # -----------------------------------------------------
    # CKD
    # -----------------------------------------------------

    if disease == "ckd":

        if feature in {
            "rbc",
            "pc",
            "pcc",
            "ba",
            "htn",
            "dm",
            "cad",
            "pe",
            "ane"
        }:

            return [0, 1]

        if feature in {
            "al",
            "su"
        }:

            return [0, 1, 2, 3, 4, 5]

        if feature == "sg":

            return [
                1.005,
                1.010,
                1.015,
                1.020,
                1.025
            ]

        if feature == "age":

            return [
                max(1, safe_int(value) - 10),
                max(1, safe_int(value) - 5),
                safe_int(value) + 5,
                safe_int(value) + 10
            ]

        if feature == "bp":

            return [
                max(40, safe_int(value) - 20),
                max(40, safe_int(value) - 10),
                safe_int(value) + 10,
                safe_int(value) + 20
            ]

        if feature == "bgr":

            return [
                max(50, safe_int(value) - 50),
                max(50, safe_int(value) - 25),
                safe_int(value) + 25,
                safe_int(value) + 50
            ]

        if feature == "bu":

            return [
                max(5, safe_int(value) - 20),
                max(5, safe_int(value) - 10),
                safe_int(value) + 10,
                safe_int(value) + 20
            ]

        if feature == "sc":

            return [
                max(0.3, safe_float(value) - 1.0),
                max(0.3, safe_float(value) - 0.5),
                safe_float(value) + 0.5,
                safe_float(value) + 1.0
            ]

        if feature == "sod":

            return [
                max(100, safe_int(value) - 10),
                max(100, safe_int(value) - 5),
                safe_int(value) + 5,
                safe_int(value) + 10
            ]

        if feature == "pot":

            return [
                max(2.0, safe_float(value) - 1.0),
                max(2.0, safe_float(value) - 0.5),
                safe_float(value) + 0.5,
                safe_float(value) + 1.0
            ]

        if feature == "hemo":

            return [
                max(3.0, safe_float(value) - 3),
                max(3.0, safe_float(value) - 1.5),
                safe_float(value) + 1.5,
                safe_float(value) + 3
            ]

        if feature == "pcv":

            return [
                max(10, safe_int(value) - 10),
                max(10, safe_int(value) - 5),
                safe_int(value) + 5,
                safe_int(value) + 10
            ]

        if feature in {
            "wbcc",
            "rbcc"
        }:

            return [
                max(1, safe_float(value) * 0.75),
                max(1, safe_float(value) * 0.9),
                safe_float(value) * 1.1,
                safe_float(value) * 1.25
            ]

        if feature == "appet":

            return [0, 1]

    # -----------------------------------------------------
    # STROKE
    # -----------------------------------------------------

    if disease == "stroke":

        if feature in {
            "hypertension",
            "heart_disease",
            "ever_married"
        }:

            return [0, 1]

        if feature == "gender":

            return [
                "Male",
                "Female",
                0,
                1
            ]

        if feature == "age":

            return [
                max(1, safe_int(value) - 10),
                max(1, safe_int(value) - 5),
                safe_int(value) + 5,
                safe_int(value) + 10
            ]

        if feature == "work_type":

            return [
                "Private",
                "Self-employed",
                "Government Job",
                "Children",
                "Never Worked"
            ]

        if feature == "Residence_type":

            return [
                "Urban",
                "Rural"
            ]

        if feature == "avg_glucose_level":

            return [
                max(
                    40,
                    safe_float(value) - 50
                ),
                max(
                    40,
                    safe_float(value) - 25
                ),
                safe_float(value) + 25,
                safe_float(value) + 50
            ]

        if feature == "bmi":

            return [
                max(
                    10,
                    safe_float(value) - 5
                ),
                max(
                    10,
                    safe_float(value) - 2
                ),
                safe_float(value) + 2,
                safe_float(value) + 5
            ]

        if feature == "smoking_status":

            return [
                "never smoked",
                "formerly smoked",
                "smokes",
                "Unknown"
            ]

    return [value]


# =========================================================
# NORMALIZE MODEL PREDICTION
# =========================================================

def extract_prediction(result):

    if not isinstance(result, dict):

        return None

    value = result.get(
        "prediction_class"
    )

    if value is None:

        value = result.get(
            "class"
        )

    if value is None:

        value = result.get(
            "prediction"
        )

    try:

        return int(value)

    except Exception:

        return None


# =========================================================
# NORMALIZE PROBABILITY
# =========================================================

def extract_probability(result):

    if not isinstance(result, dict):

        return 0.0

    value = result.get(
        "probability",
        result.get(
            "prediction_probability",
            0
        )
    )

    try:

        value = float(value)

    except Exception:

        value = 0.0

    if 0 <= value <= 1:

        value *= 100

    return value


# =========================================================
# GENERIC COUNTERFACTUAL SEARCH
# =========================================================

def generic_counterfactual_search(
    features,
    disease,
    original_prediction,
    max_results=5
):

    names = FEATURE_NAMES[disease]

    original = prepare_counterfactual_input(
        features,
        disease
    )

    candidates = []

    # -----------------------------------------------------
    # First search one-feature changes.
    # -----------------------------------------------------

    for feature in names:

        values = candidate_values(
            disease,
            feature,
            original.get(feature)
        )

        for value in values:

            if value == original.get(feature):

                continue

            candidate = dict(original)

            candidate[feature] = value

            try:

                if disease == "stroke":

                    vector = stroke_dict_to_vector(
                        candidate
                    )

                else:

                    vector = [
                        candidate[name]
                        for name in names
                    ]

                prediction_result = predict(
                    vector,
                    disease
                )

                prediction_class = extract_prediction(
                    prediction_result
                )

                if prediction_class is None:

                    continue

                if prediction_class != original_prediction:

                    probability = extract_probability(
                        prediction_result
                    )

                    changes = {

                        feature_label(feature): [

                            original.get(feature),

                            value

                        ]

                    }

                    candidates.append({

                        "changes":
                            changes,

                        "prediction":
                            prediction_class,

                        "prediction_text":
                            prediction_text_for(
                                disease,
                                prediction_class
                            ),

                        "probability":
                            probability,

                        "number_of_changes":
                            1,

                        "normalized_change":
                            calculate_change_magnitude(
                                original,
                                candidate,
                                [feature]
                            )

                    })

                    if len(candidates) >= max_results:

                        return rank_counterfactuals(
                            candidates
                        )

            except Exception as error:

                print(
                    "Generic CF candidate error:",
                    repr(error)
                )

                continue

    # -----------------------------------------------------
    # Two-feature search.
    # -----------------------------------------------------

    if len(candidates) < max_results:

        important_features = names[:]

        pair_count = 0

        for feature_a, feature_b in itertools.combinations(
            important_features,
            2
        ):

            values_a = candidate_values(
                disease,
                feature_a,
                original.get(feature_a)
            )[:3]

            values_b = candidate_values(
                disease,
                feature_b,
                original.get(feature_b)
            )[:3]

            for value_a in values_a:

                for value_b in values_b:

                    if (
                        value_a == original.get(feature_a)
                        and
                        value_b == original.get(feature_b)
                    ):

                        continue

                    candidate = dict(original)

                    candidate[feature_a] = value_a

                    candidate[feature_b] = value_b

                    try:

                        if disease == "stroke":

                            vector = stroke_dict_to_vector(
                                candidate
                            )

                        else:

                            vector = [
                                candidate[name]
                                for name in names
                            ]

                        prediction_result = predict(
                            vector,
                            disease
                        )

                        prediction_class = extract_prediction(
                            prediction_result
                        )

                        if prediction_class is None:

                            continue

                        if prediction_class != original_prediction:

                            probability = extract_probability(
                                prediction_result
                            )

                            changes = {

                                feature_label(
                                    feature_a
                                ): [

                                    original.get(
                                        feature_a
                                    ),

                                    value_a

                                ],

                                feature_label(
                                    feature_b
                                ): [

                                    original.get(
                                        feature_b
                                    ),

                                    value_b

                                ]

                            }

                            candidates.append({

                                "changes":
                                    changes,

                                "prediction":
                                    prediction_class,

                                "prediction_text":
                                    prediction_text_for(
                                        disease,
                                        prediction_class
                                    ),

                                "probability":
                                    probability,

                                "number_of_changes":
                                    2,

                                "normalized_change":
                                    calculate_change_magnitude(
                                        original,
                                        candidate,
                                        [
                                            feature_a,
                                            feature_b
                                        ]
                                    )

                            })

                            if len(candidates) >= max_results:

                                return rank_counterfactuals(
                                    candidates
                                )

                    except Exception:

                        continue

                    pair_count += 1

                    if pair_count >= 1000:

                        break

                if pair_count >= 1000:

                    break

            if pair_count >= 1000:

                break

    return rank_counterfactuals(
        candidates
    )


# =========================================================
# PREDICTION TEXT
# =========================================================

def prediction_text_for(
    disease,
    prediction_class
):

    if int(prediction_class) == 1:

        return DISEASE_DISPLAY_NAMES.get(
            disease,
            disease.title()
        )

    return (
        "No "
        + DISEASE_DISPLAY_NAMES.get(
            disease,
            disease.title()
        )
    )


# =========================================================
# CHANGE MAGNITUDE
# =========================================================

def calculate_change_magnitude(
    original,
    candidate,
    changed_features
):

    total = 0.0

    for feature in changed_features:

        old = original.get(feature)

        new = candidate.get(feature)

        try:

            old_num = float(old)
            new_num = float(new)

            total += abs(
                new_num - old_num
            )

        except Exception:

            if str(old) != str(new):

                total += 1.0

    return round(
        total,
        2
    )


# =========================================================
# RANK COUNTERFACTUALS
# =========================================================

def rank_counterfactuals(
    counterfactuals
):

    if not isinstance(
        counterfactuals,
        list
    ):

        return []

    valid = []

    for item in counterfactuals:

        if not isinstance(
            item,
            dict
        ):

            continue

        if "changes" not in item:

            continue

        valid.append(item)

    valid.sort(
        key=lambda item: (
            safe_int(
                item.get(
                    "number_of_changes",
                    999
                ),
                999
            ),
            safe_float(
                item.get(
                    "normalized_change",
                    999999
                ),
                999999
            )
        )
    )

    return valid[:5]


# =========================================================
# NORMALIZE COUNTERFACTUALS
# =========================================================

def normalize_counterfactuals(
    counterfactuals,
    disease
):

    if not isinstance(
        counterfactuals,
        list
    ):

        return []

    normalized = []

    for cf in counterfactuals:

        if not isinstance(
            cf,
            dict
        ):

            continue

        changes = cf.get(
            "changes",
            {}
        )

        if not isinstance(
            changes,
            dict
        ):

            changes = {}

        prediction_class = cf.get(
            "prediction",
            cf.get(
                "new_prediction"
            )
        )

        try:

            prediction_class = int(
                prediction_class
            )

        except Exception:

            prediction_class = None

        prediction_text = cf.get(
            "prediction_text"
        )

        if not prediction_text:

            prediction_text = prediction_text_for(
                disease,
                prediction_class
                if prediction_class is not None
                else 0
            )

        probability = cf.get(
            "probability",
            cf.get(
                "new_probability",
                0
            )
        )

        number_of_changes = cf.get(
            "number_of_changes",
            cf.get(
                "num_changes",
                len(changes)
            )
        )

        normalized_change = cf.get(
            "normalized_change",
            cf.get(
                "normalizedChange",
                0
            )
        )

        normalized.append({

            "changes":
                changes,

            "prediction":
                prediction_class,

            "prediction_text":
                prediction_text,

            "probability":
                safe_float(
                    probability
                ),

            "number_of_changes":
                safe_int(
                    number_of_changes
                ),

            "normalized_change":
                safe_float(
                    normalized_change
                )
        })

    return normalized[:5]


# =========================================================
# COMPLETE COUNTERFACTUAL ENGINE
# =========================================================

def calculate_counterfactuals(
    features,
    disease,
    original_prediction,
    original_probability,
    max_results=5
):

    # -----------------------------------------------------
    # Heart uses the existing dedicated implementation.
    # -----------------------------------------------------

    if disease == "heart":

        raw = run_heart_counterfactual(
            features,
            max_results=max_results
        )

        normalized = normalize_counterfactuals(
            raw,
            disease
        )

        if normalized:

            return {

                "original_prediction":
                    original_prediction,

                "original_probability":
                    original_probability,

                "counterfactuals":
                    normalized

            }

    # -----------------------------------------------------
    # Diabetes / CKD / Stroke use generic bounded search.
    # -----------------------------------------------------

    generic = generic_counterfactual_search(
        features,
        disease,
        original_prediction,
        max_results=max_results
    )

    return {

        "original_prediction":
            original_prediction,

        "original_probability":
            original_probability,

        "counterfactuals":
            generic

    }


# =========================================================
# RECOMMENDATION
# =========================================================

def get_recommendation(
    prediction_class,
    probability,
    disease
):

    if disease != "stroke":

        return recommendation(
            prediction_class,
            probability,
            disease
        )

    if prediction_class == 1:

        return {

            "risk":
                "High",

            "recommendation":
                "The model indicates a higher likelihood "
                "of stroke risk. Prompt consultation with a "
                "healthcare professional is strongly "
                "recommended for further clinical evaluation "
                "and appropriate diagnostic assessment."

        }

    return {

        "risk":
            "Low",

        "recommendation":
            "The model indicates a lower likelihood of "
            "stroke risk. This result should still be "
            "interpreted together with clinical assessment "
            "and professional judgement."

    }


# =========================================================
# LIME
# =========================================================

def get_lime_explanation(
    features,
    disease
):

    try:

        result = lime_explain(
            features,
            disease
        )

        if result is None:

            return []

        return result

    except Exception as error:

        print(
            "LIME explanation error:",
            repr(error)
        )

        return []


# =========================================================
# AGREEMENT NORMALIZATION
# =========================================================

def normalize_agreement(
    agreement
):

    if not isinstance(
        agreement,
        dict
    ):

        return None

    feature_agreement = agreement.get(
        "feature_agreement_percentage",
        agreement.get(
            "feature_agreement",
            agreement.get(
                "overlap",
                0
            )
        )
    )

    direction_agreement = agreement.get(
        "direction_agreement_percentage",
        agreement.get(
            "direction_agreement",
            0
        )
    )

    ranking_agreement = agreement.get(
        "ranking_agreement_percentage",
        agreement.get(
            "ranking_agreement",
            0
        )
    )

    overall_consistency = agreement.get(
        "overall_consistency_score",
        agreement.get(
            "overall_consistency",
            agreement.get(
                "score",
                0
            )
        )
    )

    consistency_level = agreement.get(
        "consistency_level"
    )

    if not consistency_level:

        if safe_float(
            overall_consistency
        ) >= 80:

            consistency_level = "High"

        elif safe_float(
            overall_consistency
        ) >= 50:

            consistency_level = "Moderate"

        else:

            consistency_level = "Low"

    common_features = agreement.get(
        "common_features",
        agreement.get(
            "shared_features",
            []
        )
    )

    shap_only = agreement.get(
        "shap_only_features",
        agreement.get(
            "shap_only",
            []
        )
    )

    lime_only = agreement.get(
        "lime_only_features",
        agreement.get(
            "lime_only",
            []
        )
    )

    return {

        # Original keys
        **agreement,

        # Main frontend score aliases
        "score":
            overall_consistency,

        "agreement_score":
            overall_consistency,

        "agreementScore":
            overall_consistency,

        "overall_score":
            overall_consistency,

        "overall_consistency":
            overall_consistency,

        "overall_consistency_score":
            overall_consistency,

        # Feature agreement
        "feature_agreement":
            feature_agreement,

        "feature_agreement_percentage":
            feature_agreement,

        "featureAgreement":
            feature_agreement,

        # Direction agreement
        "direction_agreement":
            direction_agreement,

        "direction_agreement_percentage":
            direction_agreement,

        "directionAgreement":
            direction_agreement,

        # Ranking agreement
        "ranking_agreement":
            ranking_agreement,

        "ranking_agreement_percentage":
            ranking_agreement,

        "rankingAgreement":
            ranking_agreement,

        # Level
        "consistency_level":
            consistency_level,

        "consistencyLevel":
            consistency_level,

        # Shared
        "common_features":
            common_features,

        "shared_features":
            common_features,

        "sharedFeatures":
            common_features,

        # SHAP only
        "shap_only":
            shap_only,

        "shap_only_features":
            shap_only,

        "shapOnlyFeatures":
            shap_only,

        # LIME only
        "lime_only":
            lime_only,

        "lime_only_features":
            lime_only,

        "limeOnlyFeatures":
            lime_only
    }


# =========================================================
# AGREEMENT CALCULATION
# =========================================================

def calculate_agreement(
    explanation,
    lime,
    disease
):

    if not explanation:

        return None

    if not lime:

        return None

    try:

        raw = calculate_shap_lime_agreement(
            explanation,
            lime,
            top_k=5
        )

        return normalize_agreement(
            raw
        )

    except Exception as error:

        print(
            "SHAP-LIME agreement error:",
            repr(error)
        )

        return None


# =========================================================
# COMPLETE ASSESSMENT
# =========================================================

def run_assessment(
    data,
    disease,
    features
):

    # -----------------------------------------------------
    # Prediction
    # -----------------------------------------------------

    prediction_result = predict(
        features,
        disease
    )

    if not isinstance(
        prediction_result,
        dict
    ):

        raise ValueError(
            "Prediction module returned an invalid result."
        )

    result = dict(
        prediction_result
    )

    prediction_class = extract_prediction(
        result
    )

    if prediction_class is None:

        raise ValueError(
            "Prediction class was not returned by model."
        )

    probability = extract_probability(
        result
    )

    # Keep both raw and percentage-compatible values.
    result[
        "prediction_class"
    ] = prediction_class

    result[
        "class"
    ] = prediction_class

    result[
        "probability"
    ] = probability

    # -----------------------------------------------------
    # SHAP
    # -----------------------------------------------------

    explanation = explain(
        features,
        disease
    )

    if explanation is None:

        explanation = []

    # -----------------------------------------------------
    # LIME
    # -----------------------------------------------------

    lime = get_lime_explanation(
        features,
        disease
    )

    if lime is None:

        lime = []

    # -----------------------------------------------------
    # Recommendation
    # -----------------------------------------------------

    advice = get_recommendation(
        prediction_class,
        probability,
        disease
    )

    result[
        "risk_level"
    ] = advice.get(
        "risk",
        "Unknown"
    )

    result[
        "recommendation"
    ] = advice.get(
        "recommendation",
        ""
    )

    # -----------------------------------------------------
    # Prediction text aliases
    # -----------------------------------------------------

    result[
        "prediction_text"
    ] = prediction_text_for(
        disease,
        prediction_class
    )

    result[
        "predictionText"
    ] = result[
        "prediction_text"
    ]

    # -----------------------------------------------------
    # SHAP
    # -----------------------------------------------------

    result[
        "top_features"
    ] = explanation

    result[
        "shap_features"
    ] = explanation

    result[
        "shap"
    ] = explanation

    result[
        "explanation"
    ] = explanation

    # -----------------------------------------------------
    # LIME
    # -----------------------------------------------------

    result[
        "lime_features"
    ] = lime

    result[
        "lime"
    ] = lime

    # -----------------------------------------------------
    # Agreement
    # -----------------------------------------------------

    agreement = calculate_agreement(
        explanation,
        lime,
        disease
    )

    result[
        "agreement"
    ] = agreement

    result[
        "shap_lime_agreement"
    ] = agreement

    result[
        "explanation_agreement"
    ] = agreement

    # -----------------------------------------------------
    # Counterfactual
    # -----------------------------------------------------

    cf_result = calculate_counterfactuals(
        features,
        disease,
        prediction_class,
        probability,
        max_results=5
    )

    counterfactuals = cf_result.get(
        "counterfactuals",
        []
    )

    result[
        "counterfactuals"
    ] = counterfactuals

    result[
        "counterfactual_explanations"
    ] = counterfactuals

    result[
        "counterfactual_original_prediction"
    ] = cf_result.get(
        "original_prediction"
    )

    result[
        "counterfactual_original_probability"
    ] = cf_result.get(
        "original_probability"
    )

    # -----------------------------------------------------
    # Patient
    # -----------------------------------------------------

    patient = build_patient_data(
        data,
        features,
        disease
    )

    result[
        "patient"
    ] = patient

    result[
        "disease"
    ] = disease

    result[
        "disease_display_name"
    ] = DISEASE_DISPLAY_NAMES[
        disease
    ]

    return patient, result


# =========================================================
# HOME
# =========================================================

@app.route(
    "/",
    methods=["GET"]
)
def home():

    return jsonify({

        "project":
            "Explainable AI Clinical Decision Support System",

        "status":
            "Running",

        "supported_diseases":
            SUPPORTED_DISEASES,

        "expected_features":
            EXPECTED_FEATURES,

        "features":
            FEATURE_NAMES,

        "version":
            "5.0"

    })


# =========================================================
# PREDICT
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

        data = request.get_json(
            silent=True
        )

        if not data:

            return jsonify({

                "success":
                    False,

                "error":
                    "Invalid JSON data."

            }), 400

        disease = normalize_disease(
            data.get(
                "disease",
                "heart"
            )
        )

        if disease not in SUPPORTED_DISEASES:

            return jsonify({

                "success":
                    False,

                "error":
                    "Unsupported disease. "
                    "Use heart, diabetes, ckd, or stroke."

            }), 400

        if "features" not in data:

            return jsonify({

                "success":
                    False,

                "error":
                    "Missing 'features' field."

            }), 400

        features = data[
            "features"
        ]

        validate_features(
            features,
            disease
        )

        patient, result = run_assessment(
            data,
            disease,
            features
        )

        save_prediction(
            patient,
            result
        )

        print()
        print("=" * 70)
        print(
            "PREDICTION RESPONSE READY"
        )
        print("=" * 70)

        print(
            "Disease:",
            disease
        )

        print(
            "Prediction:",
            result.get(
                "prediction"
            )
        )

        print(
            "Prediction Class:",
            result.get(
                "prediction_class"
            )
        )

        print(
            "Probability:",
            result.get(
                "probability"
            )
        )

        print(
            "SHAP features:",
            len(
                result.get(
                    "top_features",
                    []
                )
            )
        )

        print(
            "LIME features:",
            len(
                result.get(
                    "lime_features",
                    []
                )
            )
        )

        agreement = result.get(
            "agreement"
        )

        if agreement:

            print(
                "Agreement Score:",
                agreement.get(
                    "overall_consistency_score",
                    agreement.get(
                        "score",
                        0
                    )
                )
            )

        else:

            print(
                "Agreement:",
                "NOT AVAILABLE"
            )

        print(
            "Counterfactuals:",
            len(
                result.get(
                    "counterfactuals",
                    []
                )
            )
        )

        print("=" * 70)

        return jsonify(
            result
        ), 200

    except Exception as error:

        print(
            "Prediction Error:",
            repr(error)
        )

        return jsonify({

            "success":
                False,

            "error":
                str(error)

        }), 500


# =========================================================
# CLINICAL REPORT
# =========================================================

@app.route(
    "/report",
    methods=["POST"]
)
@role_required(
    "doctor",
    "staff"
)
def report():

    try:

        data = request.get_json(
            silent=True
        )

        if not data:

            return jsonify({

                "success":
                    False,

                "error":
                    "Invalid JSON data."

            }), 400

        disease = normalize_disease(
            data.get(
                "disease",
                "heart"
            )
        )

        if disease not in SUPPORTED_DISEASES:

            return jsonify({

                "success":
                    False,

                "error":
                    "Unsupported disease."

            }), 400

        if "features" not in data:

            return jsonify({

                "success":
                    False,

                "error":
                    "Missing 'features' field."

            }), 400

        features = data[
            "features"
        ]

        validate_features(
            features,
            disease
        )

        patient, generated_result = run_assessment(
            data,
            disease,
            features
        )

        # -------------------------------------------------
        # Preserve supplied SHAP data.
        # -------------------------------------------------

        supplied_shap = (
            data.get("top_features")
            or
            data.get("shap_features")
            or
            data.get("explanation")
        )

        if supplied_shap:

            generated_result[
                "top_features"
            ] = supplied_shap

            generated_result[
                "shap_features"
            ] = supplied_shap

            generated_result[
                "explanation"
            ] = supplied_shap

        # -------------------------------------------------
        # Preserve supplied LIME.
        # -------------------------------------------------

        supplied_lime = (
            data.get("lime_features")
            or
            data.get("lime")
        )

        if supplied_lime:

            generated_result[
                "lime_features"
            ] = supplied_lime

            generated_result[
                "lime"
            ] = supplied_lime

        # -------------------------------------------------
        # Preserve agreement.
        # -------------------------------------------------

        supplied_agreement = (
            data.get(
                "agreement"
            )
            or
            data.get(
                "shap_lime_agreement"
            )
            or
            data.get(
                "explanation_agreement"
            )
        )

        if supplied_agreement:

            normalized = normalize_agreement(
                supplied_agreement
            )

            generated_result[
                "agreement"
            ] = normalized

            generated_result[
                "shap_lime_agreement"
            ] = normalized

            generated_result[
                "explanation_agreement"
            ] = normalized

        # -------------------------------------------------
        # Preserve counterfactuals.
        # -------------------------------------------------

        supplied_counterfactuals = (
            data.get(
                "counterfactuals"
            )
            or
            data.get(
                "counterfactual_explanations"
            )
            or
            []
        )

        if supplied_counterfactuals:

            normalized_cf = normalize_counterfactuals(
                supplied_counterfactuals,
                disease
            )

            generated_result[
                "counterfactuals"
            ] = normalized_cf

            generated_result[
                "counterfactual_explanations"
            ] = normalized_cf

        # -------------------------------------------------
        # Report directory.
        # -------------------------------------------------

        reports_dir = os.path.join(
            os.path.dirname(
                os.path.abspath(
                    __file__
                )
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

        generate_report(
            patient,
            generated_result,
            output_path
        )

        return send_file(
            output_path,
            as_attachment=True,
            download_name=(
                disease
                + "_Clinical_Report.pdf"
            ),
            mimetype="application/pdf"
        )

    except Exception as error:

        print(
            "Report Error:",
            repr(error)
        )

        return jsonify({

            "success":
                False,

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

        if not isinstance(
            history_data,
            list
        ):

            history_data = []

        total_cases = len(
            history_data
        )

        high_risk = sum(

            1

            for item in history_data

            if str(
                item.get(
                    "risk_level",
                    ""
                )
            ).lower()
            == "high"

        )

        low_risk = sum(

            1

            for item in history_data

            if str(
                item.get(
                    "risk_level",
                    ""
                )
            ).lower()
            == "low"

        )

        return jsonify({

            "success":
                True,

            "cases_processed":
                total_cases,

            "high_risk_flags":
                high_risk,

            "low_risk_cases":
                low_risk

        }), 200

    except Exception as error:

        print(
            "Statistics Error:",
            repr(error)
        )

        return jsonify({

            "success":
                False,

            "error":
                str(error)

        }), 500


# =========================================================
# HISTORY
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

        if history_data is None:

            history_data = []

        return jsonify(
            history_data
        ), 200

    except Exception as error:

        print(
            "History Error:",
            repr(error)
        )

        return jsonify({

            "success":
                False,

            "error":
                str(error)

        }), 500


# =========================================================
# ERROR HANDLERS
# =========================================================

@app.errorhandler(
    404
)
def not_found(error):

    return jsonify({

        "success":
            False,

        "error":
            "Endpoint not found."

    }), 404


@app.errorhandler(
    405
)
def method_not_allowed(error):

    return jsonify({

        "success":
            False,

        "error":
            "Method not allowed."

    }), 405


@app.errorhandler(
    500
)
def internal_server_error(error):

    return jsonify({

        "success":
            False,

        "error":
            "Internal server error."

    }), 500


# =========================================================
# APPLICATION START
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
        debug=False,
        use_reloader=False
    )