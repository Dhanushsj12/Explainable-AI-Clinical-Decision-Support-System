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

heart_df = pd.read_csv(
    os.path.join(
        BASE_DIR,
        "datasets",
        "processed",
        "heart_preprocessed.csv"
    )
)

heart_X_train = heart_df.drop(
    "target",
    axis=1
)

heart_X_train_scaled = heart_scaler.transform(
    heart_X_train
)

heart_feature_names = (
    heart_X_train.columns.tolist()
)


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

diabetes_X_train_scaled = diabetes_df

diabetes_feature_names = (
    diabetes_df.columns.tolist()
)


diabetes_explainer = LimeTabularExplainer(

    training_data=diabetes_X_train_scaled.values,

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

ckd_X_train_scaled = ckd_df

ckd_feature_names = (
    ckd_df.columns.tolist()
)


ckd_explainer = LimeTabularExplainer(

    training_data=ckd_X_train_scaled.values,

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

    patient_scaled = stroke_scaler.transform(
        processed_df
    )

    return patient_scaled


# ==========================================
# LIME Function
# ==========================================

def lime_explain(features, disease="heart"):

    # ======================================
    # Heart Disease
    # ======================================

    if disease == "heart":

        patient = np.array(
            features
        ).reshape(1, -1)

        patient_scaled = (
            heart_scaler.transform(
                patient
            )
        )

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