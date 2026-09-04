import os
import pandas as pd
import joblib
import shap


# ==========================================
# Base Directory
# ==========================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)


# ==========================================
# Load Heart Disease Model
# ==========================================

heart_model = joblib.load(
    os.path.join(
        BASE_DIR,
        "models",
        "best_model.pkl"
    )
)

heart_scaler = joblib.load(
    os.path.join(
        BASE_DIR,
        "models",
        "scaler.pkl"
    )
)


# ==========================================
# Load Diabetes Model
# ==========================================

diabetes_model = joblib.load(
    os.path.join(
        BASE_DIR,
        "models",
        "diabetes",
        "best_model.pkl"
    )
)

diabetes_scaler = joblib.load(
    os.path.join(
        BASE_DIR,
        "models",
        "diabetes_scaler.pkl"
    )
)


# ==========================================
# Load CKD Model
# ==========================================

ckd_model = joblib.load(
    os.path.join(
        BASE_DIR,
        "models",
        "ckd",
        "best_model.pkl"
    )
)

ckd_scaler = joblib.load(
    os.path.join(
        BASE_DIR,
        "models",
        "ckd",
        "scaler.pkl"
    )
)


# ==========================================
# Heart Disease Data
# ==========================================

heart_df = pd.read_csv(
    os.path.join(
        BASE_DIR,
        "datasets",
        "processed",
        "heart_preprocessed.csv"
    )
)

heart_X = heart_df.drop(
    "target",
    axis=1
)

heart_feature_names = heart_X.columns.tolist()


# ==========================================
# Diabetes Data
# ==========================================

diabetes_X = pd.read_csv(
    os.path.join(
        BASE_DIR,
        "datasets",
        "processed",
        "diabetes",
        "x_train.csv"
    )
)

diabetes_feature_names = (
    diabetes_X.columns.tolist()
)


# ==========================================
# CKD Data
# ==========================================

ckd_X = pd.read_csv(
    os.path.join(
        BASE_DIR,
        "datasets",
        "processed",
        "ckd",
        "x_train.csv"
    )
)

ckd_feature_names = (
    ckd_X.columns.tolist()
)


# ==========================================
# Feature Labels
# ==========================================

HEART_FEATURE_LABELS = {

    "age": "Age",
    "sex": "Sex",
    "cp": "Chest Pain Type",
    "trestbps": "Resting Blood Pressure",
    "chol": "Serum Cholesterol",
    "fbs": "Fasting Blood Sugar",
    "restecg": "Resting ECG",
    "thalach": "Maximum Heart Rate",
    "exang": "Exercise Induced Angina",
    "oldpeak": "ST Depression",
    "slope": "Slope of ST Segment",
    "ca": "Major Vessels",
    "thal": "Thalassemia"

}


DIABETES_FEATURE_LABELS = {

    "Age": "Age",
    "Gender": "Gender",
    "Polyuria": "Polyuria",
    "Polydipsia": "Polydipsia",
    "sudden weight loss": "Sudden Weight Loss",
    "weakness": "Weakness",
    "Polyphagia": "Polyphagia",
    "Genital thrush": "Genital Thrush",
    "visual blurring": "Visual Blurring",
    "Itching": "Itching",
    "Irritability": "Irritability",
    "delayed healing": "Delayed Healing",
    "partial paresis": "Partial Paresis",
    "muscle stiffness": "Muscle Stiffness",
    "Alopecia": "Alopecia",
    "Obesity": "Obesity"

}


CKD_FEATURE_LABELS = {

    "age": "Age",
    "bp": "Blood Pressure",
    "sg": "Specific Gravity",
    "al": "Albumin",
    "su": "Sugar",
    "rbc": "Red Blood Cells",
    "pc": "Pus Cell",
    "pcc": "Pus Cell Clumps",
    "ba": "Bacteria",
    "bgr": "Blood Glucose Random",
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
    "ane": "Anemia"

}


# ==========================================
# Create SHAP Explainers
# ==========================================

heart_explainer = shap.TreeExplainer(
    heart_model
)

diabetes_explainer = shap.TreeExplainer(
    diabetes_model
)

ckd_explainer = shap.TreeExplainer(
    ckd_model
)


# ==========================================
# SHAP Explanation Function
# ==========================================

def explain(features, disease="heart"):

    # ======================================
    # Heart Disease
    # ======================================

    if disease == "heart":

        patient_df = pd.DataFrame(
            [features],
            columns=heart_feature_names
        )

        patient_scaled = heart_scaler.transform(
            patient_df
        )

        shap_values = heart_explainer(
            patient_scaled
        )

        values = shap_values.values[0]

        if len(values.shape) > 1:
            values = values[:, 1]

        explanation = []

        for feature, impact in zip(
            heart_feature_names,
            values
        ):

            explanation.append({

                "feature":
                    HEART_FEATURE_LABELS.get(
                        feature,
                        feature
                    ),

                "impact":
                    round(
                        float(impact),
                        4
                    )

            })


    # ======================================
    # Diabetes
    # ======================================

    elif disease == "diabetes":

        patient_df = pd.DataFrame(
            [features],
            columns=diabetes_feature_names
        )

        patient_scaled = diabetes_scaler.transform(
            patient_df
        )

        shap_values = diabetes_explainer(
            patient_scaled
        )

        values = shap_values.values[0]

        if len(values.shape) > 1:
            values = values[:, 1]

        explanation = []

        for feature, impact in zip(
            diabetes_feature_names,
            values
        ):

            explanation.append({

                "feature":
                    DIABETES_FEATURE_LABELS.get(
                        feature,
                        feature
                    ),

                "impact":
                    round(
                        float(impact),
                        4
                    )

            })


    # ======================================
    # CKD
    # ======================================

    elif disease == "ckd":

        patient_df = pd.DataFrame(
            [features],
            columns=ckd_feature_names
        )

        patient_scaled = ckd_scaler.transform(
            patient_df
        )

        shap_values = ckd_explainer(
            patient_scaled
        )

        values = shap_values.values[0]

        # Handle binary classification
        if len(values.shape) > 1:
            values = values[:, 1]

        explanation = []

        for feature, impact in zip(
            ckd_feature_names,
            values
        ):

            explanation.append({

                "feature":
                    CKD_FEATURE_LABELS.get(
                        feature,
                        feature
                    ),

                "impact":
                    round(
                        float(impact),
                        4
                    )

            })


    # ======================================
    # Invalid Disease
    # ======================================

    else:

        raise ValueError(
            f"Unsupported disease: {disease}"
        )


    # ======================================
    # Sort by Importance
    # ======================================

    explanation.sort(

        key=lambda x:
            abs(x["impact"]),

        reverse=True

    )


    # ======================================
    # Return Top 5
    # ======================================

    return explanation[:5]