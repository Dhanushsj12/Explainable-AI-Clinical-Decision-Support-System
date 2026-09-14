import os
import numpy as np
import pandas as pd

from lime.lime_tabular import LimeTabularExplainer

from model_loader import (
    heart_model,
    heart_scaler,

    diabetes_model,
    diabetes_scaler,

    ckd_model,
    ckd_scaler,

    stroke_model,
    stroke_scaler,
    stroke_imputer,
    stroke_feature_names
)


# ==========================================
# Base Directory
# ==========================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)


# ==========================================
# Heart Disease LIME
# ==========================================
#
# IMPORTANT:
# The final Heart model was trained using:
#
#   242 real training rows
#   + 5,000 synthetic rows
#   = 5,242 training rows
#
# Therefore, LIME should use the same
# real + synthetic training distribution
# as its background data.
#
# The test set is NOT used here.
# ==========================================


HEART_REAL_TRAIN_FILE = os.path.join(
    BASE_DIR,
    "datasets",
    "augmented",
    "heart",
    "heart_train_real.csv"
)

HEART_SYNTHETIC_TRAIN_FILE = os.path.join(
    BASE_DIR,
    "datasets",
    "augmented",
    "heart",
    "heart_train_synthetic.csv"
)


# ==========================================
# Load Real Heart Training Data
# ==========================================

heart_real_df = pd.read_csv(
    HEART_REAL_TRAIN_FILE
)


# ==========================================
# Load Synthetic Heart Training Data
# ==========================================

heart_synthetic_df = pd.read_csv(
    HEART_SYNTHETIC_TRAIN_FILE
)


# ==========================================
# Remove data_source Column
# ==========================================

if "data_source" in heart_real_df.columns:

    heart_real_df = heart_real_df.drop(
        columns=["data_source"]
    )


if "data_source" in heart_synthetic_df.columns:

    heart_synthetic_df = heart_synthetic_df.drop(
        columns=["data_source"]
    )


# ==========================================
# Heart Feature Names
# ==========================================

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


# ==========================================
# Select Heart Features Only
# ==========================================

heart_real_X = heart_real_df[
    HEART_FEATURES
]

heart_synthetic_X = heart_synthetic_df[
    HEART_FEATURES
]


# ==========================================
# Combine Real + Synthetic Data
# ==========================================

heart_X_train = pd.concat(
    [
        heart_real_X,
        heart_synthetic_X
    ],
    ignore_index=True
)


# ==========================================
# Make Sure Feature Order Is Correct
# ==========================================

heart_X_train = heart_X_train[
    HEART_FEATURES
]


# ==========================================
# Convert to Numeric
# ==========================================

heart_X_train = heart_X_train.apply(
    pd.to_numeric,
    errors="coerce"
)


# ==========================================
# Handle Missing Values
# ==========================================

if heart_X_train.isnull().any().any():

    heart_X_train = heart_X_train.fillna(
        heart_X_train.median()
    )


# ==========================================
# Scale Heart Training Data
# ==========================================

heart_X_train_scaled = (
    heart_scaler.transform(
        heart_X_train
    )
)


# ==========================================
# Heart LIME Feature Names
# ==========================================

heart_feature_names = (
    HEART_FEATURES
)


# ==========================================
# Create Heart LIME Explainer
# ==========================================

heart_explainer = LimeTabularExplainer(

    training_data=heart_X_train_scaled,

    feature_names=heart_feature_names,

    class_names=[
        "No Heart Disease",
        "Heart Disease"
    ],

    mode="classification",

    random_state=42
)


# ==========================================
# Diabetes LIME
# ==========================================

diabetes_df = pd.read_csv(
    os.path.join(
        BASE_DIR,
        "datasets",
        "processed",
        "diabetes",
        "x_train.csv"
    )
)


diabetes_X_train_scaled = (
    diabetes_df
)


diabetes_feature_names = (
    diabetes_df.columns.tolist()
)


diabetes_explainer = LimeTabularExplainer(

    training_data=(
        diabetes_X_train_scaled.values
    ),

    feature_names=diabetes_feature_names,

    class_names=[
        "Negative",
        "Positive"
    ],

    mode="classification",

    random_state=42
)


# ==========================================
# CKD LIME
# ==========================================

ckd_df = pd.read_csv(
    os.path.join(
        BASE_DIR,
        "datasets",
        "processed",
        "ckd",
        "x_train.csv"
    )
)


ckd_X_train_scaled = (
    ckd_df
)


ckd_feature_names = (
    ckd_df.columns.tolist()
)


ckd_explainer = LimeTabularExplainer(

    training_data=(
        ckd_X_train_scaled.values
    ),

    feature_names=ckd_feature_names,

    class_names=[
        "Not CKD",
        "CKD"
    ],

    mode="classification",

    random_state=42
)


# ==========================================
# Stroke LIME
# ==========================================

stroke_x_train_path = os.path.join(
    BASE_DIR,
    "datasets",
    "processed",
    "stroke",
    "x_train.csv"
)


stroke_X_train_scaled = pd.read_csv(
    stroke_x_train_path
)


stroke_X_train_scaled = (
    stroke_X_train_scaled.values
)


stroke_explainer = LimeTabularExplainer(

    training_data=stroke_X_train_scaled,

    feature_names=stroke_feature_names,

    class_names=[
        "No Stroke",
        "Stroke"
    ],

    mode="classification",

    random_state=42
)


# ==========================================
# Stroke Preprocessing
# ==========================================

STROKE_NUMERIC_FEATURES = [
    "age",
    "hypertension",
    "heart_disease",
    "avg_glucose_level",
    "bmi"
]


STROKE_CATEGORICAL_FEATURES = [
    "gender",
    "ever_married",
    "work_type",
    "Residence_type",
    "smoking_status"
]


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


def preprocess_stroke_for_lime(features):

    # --------------------------------------
    # Support dictionary input
    # --------------------------------------

    if isinstance(features, dict):

        features = [
            features[column]
            for column in STROKE_RAW_FEATURES
        ]

    # --------------------------------------
    # Validate feature count
    # --------------------------------------

    if len(features) != 10:

        raise ValueError(
            "Stroke requires exactly 10 features"
        )

    # --------------------------------------
    # Create DataFrame
    # --------------------------------------

    patient_df = pd.DataFrame(
        [features],
        columns=STROKE_RAW_FEATURES
    )

    # --------------------------------------
    # Numeric conversion
    # --------------------------------------

    for column in STROKE_NUMERIC_FEATURES:

        patient_df[column] = pd.to_numeric(
            patient_df[column],
            errors="coerce"
        )

    # --------------------------------------
    # Impute numerical values
    # --------------------------------------

    patient_df[
        STROKE_NUMERIC_FEATURES
    ] = stroke_imputer.transform(
        patient_df[
            STROKE_NUMERIC_FEATURES
        ]
    )

    # --------------------------------------
    # One-hot encode categorical values
    # --------------------------------------

    categorical_df = pd.get_dummies(
        patient_df[
            STROKE_CATEGORICAL_FEATURES
        ],
        drop_first=False
    )

    # --------------------------------------
    # Combine numerical + categorical
    # --------------------------------------

    numerical_df = patient_df[
        STROKE_NUMERIC_FEATURES
    ]

    processed_df = pd.concat(
        [
            numerical_df,
            categorical_df
        ],
        axis=1
    )

    # --------------------------------------
    # Match training feature order
    # --------------------------------------

    processed_df = processed_df.reindex(
        columns=stroke_feature_names,
        fill_value=0
    )

    # --------------------------------------
    # Convert to float
    # --------------------------------------

    processed_df = processed_df.astype(
        float
    )

    # --------------------------------------
    # Scale using training scaler
    # --------------------------------------

    patient_scaled = (
        stroke_scaler.transform(
            processed_df
        )
    )

    return patient_scaled


# ==========================================
# LIME Function
# ==========================================

def lime_explain(
    features,
    disease="heart"
):

    # ======================================
    # Heart Disease
    # ======================================

    if disease == "heart":

        patient = np.array(
            features,
            dtype=float
        ).reshape(1, -1)

        # ----------------------------------
        # Validate feature count
        # ----------------------------------

        if patient.shape[1] != len(
            HEART_FEATURES
        ):

            raise ValueError(
                "Heart Disease requires "
                "exactly 13 features"
            )

        # ----------------------------------
        # Create DataFrame
        # ----------------------------------

        patient_df = pd.DataFrame(
            patient,
            columns=HEART_FEATURES
        )

        # ----------------------------------
        # Scale using final heart scaler
        # ----------------------------------

        patient_scaled = (
            heart_scaler.transform(
                patient_df
            )
        )

        # ----------------------------------
        # Generate LIME explanation
        # ----------------------------------

        explanation = (
            heart_explainer.explain_instance(

                patient_scaled[0],

                heart_model.predict_proba,

                num_features=5
            )
        )


    # ======================================
    # Diabetes
    # ======================================

    elif disease == "diabetes":

        patient = np.array(
            features
        ).reshape(1, -1)

        patient_scaled = (
            diabetes_scaler.transform(
                patient
            )
        )

        explanation = (
            diabetes_explainer.explain_instance(

                patient_scaled[0],

                diabetes_model.predict_proba,

                num_features=5
            )
        )


    # ======================================
    # CKD
    # ======================================

    elif disease == "ckd":

        patient = np.array(
            features
        ).reshape(1, -1)

        patient_scaled = (
            ckd_scaler.transform(
                patient
            )
        )

        explanation = (
            ckd_explainer.explain_instance(

                patient_scaled[0],

                ckd_model.predict_proba,

                num_features=5
            )
        )


    # ======================================
    # Stroke
    # ======================================

    elif disease == "stroke":

        patient_scaled = (
            preprocess_stroke_for_lime(
                features
            )
        )

        explanation = (
            stroke_explainer.explain_instance(

                patient_scaled[0],

                stroke_model.predict_proba,

                num_features=5
            )
        )


    # ======================================
    # Invalid Disease
    # ======================================

    else:

        raise ValueError(
            f"Unsupported disease: {disease}"
        )


    # ======================================
    # Convert Explanation
    # ======================================

    result = []

    for feature, weight in (
        explanation.as_list()
    ):

        result.append({

            "feature": feature,

            "impact": round(
                float(weight),
                4
            )

        })


    return result