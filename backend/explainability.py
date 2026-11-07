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
# Load Stroke Model
# ==========================================

stroke_model = joblib.load(
    os.path.join(
        BASE_DIR,
        "models",
        "stroke",
        "best_model.pkl"
    )
)

stroke_scaler = joblib.load(
    os.path.join(
        BASE_DIR,
        "models",
        "stroke",
        "scaler.pkl"
    )
)

stroke_imputer = joblib.load(
    os.path.join(
        BASE_DIR,
        "models",
        "stroke",
        "imputer.pkl"
    )
)

stroke_feature_names = joblib.load(
    os.path.join(
        BASE_DIR,
        "models",
        "stroke",
        "feature_names.pkl"
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

diabetes_feature_names = diabetes_X.columns.tolist()


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

ckd_feature_names = ckd_X.columns.tolist()


# ==========================================
# Stroke Data
# ==========================================

stroke_X = pd.read_csv(
    os.path.join(
        BASE_DIR,
        "datasets",
        "processed",
        "stroke",
        "x_train.csv"
    )
)


# ==========================================
# Stroke Raw Feature Names
# ==========================================

STROKE_RAW_FEATURES = [
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


# ==========================================
# Stroke Numerical Features
# ==========================================

STROKE_NUMERIC_FEATURES = [
    "age",
    "hypertension",
    "heart_disease",
    "avg_glucose_level",
    "bmi"
]


# ==========================================
# Stroke Categorical Features
# ==========================================

STROKE_CATEGORICAL_FEATURES = [
    "gender",
    "ever_married",
    "work_type",
    "Residence_type",
    "smoking_status"
]


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


STROKE_FEATURE_LABELS = {
    "age": "Age",
    "hypertension": "Hypertension",
    "heart_disease": "Heart Disease",
    "avg_glucose_level": "Average Glucose Level",
    "bmi": "Body Mass Index",

    "gender_Female": "Gender - Female",
    "gender_Male": "Gender - Male",
    "gender_Other": "Gender - Other",

    "ever_married_No": "Marital Status - No",
    "ever_married_Yes": "Marital Status - Yes",

    "work_type_Govt_job": "Work Type - Government Job",
    "work_type_Never_worked": "Work Type - Never Worked",
    "work_type_Private": "Work Type - Private",
    "work_type_Self-employed": "Work Type - Self-employed",
    "work_type_children": "Work Type - Children",

    "Residence_type_Rural": "Residence Type - Rural",
    "Residence_type_Urban": "Residence Type - Urban",

    "smoking_status_Unknown": "Smoking Status - Unknown",
    "smoking_status_formerly smoked": "Smoking Status - Formerly Smoked",
    "smoking_status_never smoked": "Smoking Status - Never Smoked",
    "smoking_status_smokes": "Smoking Status - Smokes"
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

stroke_explainer = shap.LinearExplainer(
    stroke_model,
    stroke_X
)


# ==========================================
# Stroke Preprocessing for SHAP
# ==========================================

def preprocess_stroke_for_shap(features):
    """
    Convert raw Stroke patient data into the same
    21-feature scaled format used by the Stroke model.

    Accepts either:
        1. Dictionary
        2. List / Tuple
    """

    # --------------------------------------
    # Convert dictionary to ordered list
    # --------------------------------------

    if isinstance(features, dict):

        features = [
            features.get(feature)
            for feature in STROKE_RAW_FEATURES
        ]


    # --------------------------------------
    # Validate input type
    # --------------------------------------

    if not isinstance(features, (list, tuple)):

        raise ValueError(
            "Stroke features must be provided as a dictionary or list."
        )


    # --------------------------------------
    # Validate number of features
    # --------------------------------------

    if len(features) != len(STROKE_RAW_FEATURES):

        raise ValueError(
            f"Stroke requires {len(STROKE_RAW_FEATURES)} features, "
            f"but received {len(features)}."
        )


    # --------------------------------------
    # Create DataFrame
    # --------------------------------------

    patient_df = pd.DataFrame(
        [features],
        columns=STROKE_RAW_FEATURES
    )


    # --------------------------------------
    # Convert numerical features
    # --------------------------------------

    for column in STROKE_NUMERIC_FEATURES:

        patient_df[column] = pd.to_numeric(
            patient_df[column],
            errors="coerce"
        )


    # --------------------------------------
    # Apply trained numerical imputer
    # --------------------------------------

    patient_df[STROKE_NUMERIC_FEATURES] = (
        stroke_imputer.transform(
            patient_df[STROKE_NUMERIC_FEATURES]
        )
    )


    # --------------------------------------
    # One-hot encode categorical columns
    #
    # IMPORTANT:
    # Keep the numerical columns.
    # This must match prediction.py.
    # --------------------------------------

    patient_encoded = pd.get_dummies(
        patient_df,
        columns=STROKE_CATEGORICAL_FEATURES,
        drop_first=False
    )


    # --------------------------------------
    # Match exact training feature order
    # --------------------------------------

    patient_encoded = patient_encoded.reindex(
        columns=stroke_feature_names,
        fill_value=0
    )


    # --------------------------------------
    # Convert all values to float
    # --------------------------------------

    patient_encoded = patient_encoded.astype(float)


    # --------------------------------------
    # Apply trained scaler
    # --------------------------------------

    patient_scaled = stroke_scaler.transform(
        patient_encoded
    )


    # --------------------------------------
    # Return processed data
    # --------------------------------------

    return patient_scaled


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
                "feature": HEART_FEATURE_LABELS.get(
                    feature,
                    feature
                ),
                "impact": round(
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
                "feature": DIABETES_FEATURE_LABELS.get(
                    feature,
                    feature
                ),
                "impact": round(
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

        patient_scaled = ckd_scaler.transform(patient_df)

        shap_values = ckd_explainer(
        patient_scaled
)

        values = shap_values.values[0]

        if len(values.shape) > 1:

            values = values[:, 1]

        explanation = []

        for feature, impact in zip(
            ckd_feature_names,
            values
        ):

            explanation.append({
                "feature": CKD_FEATURE_LABELS.get(
                    feature,
                    feature
                ),
                "impact": round(
                    float(impact),
                    4
                )
            })


    # ======================================
    # Stroke
    # ======================================

    elif disease == "stroke":

        # ----------------------------------
        # Convert raw Stroke input into
        # exactly the same representation
        # used by the Stroke prediction model.
        # ----------------------------------

        patient_scaled = preprocess_stroke_for_shap(
            features
        )


        # ----------------------------------
        # Generate SHAP explanation
        # ----------------------------------

        shap_values = stroke_explainer(
            patient_scaled
        )


        # ----------------------------------
        # Get SHAP values for patient
        # ----------------------------------

        values = shap_values.values[0]


        # ----------------------------------
        # Handle multi-output SHAP values
        # ----------------------------------

        if len(values.shape) > 1:

            values = values[:, 1]


        # ----------------------------------
        # Create explanation list
        # ----------------------------------

        explanation = []

        for feature, impact in zip(
            stroke_feature_names,
            values
        ):

            explanation.append({
                "feature": STROKE_FEATURE_LABELS.get(
                    feature,
                    feature
                ),
                "impact": round(
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
    # Sort by Absolute Importance
    # ======================================

    explanation.sort(
        key=lambda x: abs(x["impact"]),
        reverse=True
    )


    # ======================================
    # Return Top 5 Features
    # ======================================

    return explanation[:5]
