import numpy as np
import pandas as pd

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
    stroke_feature_names,
    stroke_threshold
)


# ============================================================
# HEART DISEASE FEATURE NAMES
# ============================================================

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


# ============================================================
# CKD FEATURE NAMES
# ============================================================

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


# ============================================================
# STROKE RAW FEATURE NAMES
# ============================================================

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


# ============================================================
# HEART DISEASE PREDICTION
# ============================================================

def predict_heart(patient_data):

    # --------------------------------------------------------
    # Create DataFrame using exact training feature names
    # --------------------------------------------------------

    patient = pd.DataFrame(
        [patient_data],
        columns=HEART_FEATURES
    )

    # --------------------------------------------------------
    # Convert values to numeric
    # --------------------------------------------------------

    patient = patient.apply(
        pd.to_numeric,
        errors="coerce"
    )

    # --------------------------------------------------------
    # Validate number of features
    # --------------------------------------------------------

    if len(patient_data) != len(HEART_FEATURES):
        raise ValueError(
            f"Heart Disease model expects "
            f"{len(HEART_FEATURES)} features, "
            f"but received {len(patient_data)}."
        )

    # --------------------------------------------------------
    # Check for invalid values
    # --------------------------------------------------------

    if patient.isnull().any().any():
        raise ValueError(
            "Invalid or missing values in Heart Disease input."
        )

    # --------------------------------------------------------
    # Scale using final 5K augmented model scaler
    # --------------------------------------------------------

    patient_scaled = heart_scaler.transform(
        patient
    )

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    prediction = int(
        heart_model.predict(
            patient_scaled
        )[0]
    )

    # --------------------------------------------------------
    # Probability
    # --------------------------------------------------------

    probability = float(
        heart_model.predict_proba(
            patient_scaled
        )[0][1]
    )

    # --------------------------------------------------------
    # Disease label
    # --------------------------------------------------------

    disease = (
        "No Heart Disease"
        if prediction == 0
        else "Heart Disease"
    )

    # --------------------------------------------------------
    # Confidence
    # --------------------------------------------------------

    confidence = round(
        probability * 100,
        2
    )

    return {
        "prediction_class": prediction,
        "prediction": disease,
        "probability": confidence
    }


# ============================================================
# DIABETES PREDICTION
# ============================================================

def predict_diabetes(patient_data):

    patient = np.array(
        patient_data
    ).reshape(1, -1)

    patient_scaled = diabetes_scaler.transform(
        patient
    )

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    prediction = int(
        diabetes_model.predict(
            patient_scaled
        )[0]
    )

    # --------------------------------------------------------
    # Probability
    # --------------------------------------------------------

    probability = float(
        diabetes_model.predict_proba(
            patient_scaled
        )[0][1]
    )

    # --------------------------------------------------------
    # Disease label
    # --------------------------------------------------------

    disease = (
        "No Diabetes"
        if prediction == 0
        else "Diabetes"
    )

    confidence = round(
        probability * 100,
        2
    )

    return {
        "prediction_class": prediction,
        "prediction": disease,
        "probability": confidence
    }


# ============================================================
# CKD PREDICTION
# ============================================================

def predict_ckd(patient_data):

    # --------------------------------------------------------
    # Create DataFrame using exact CKD feature names
    # --------------------------------------------------------

    patient = pd.DataFrame(
        [patient_data],
        columns=CKD_FEATURES
    )
    patient_scaled = ckd_scaler.transform(patient)

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    prediction = int(
        ckd_model.predict(
            patient_scaled
        )[0]
    )

    # --------------------------------------------------------
    # Probability
    # --------------------------------------------------------

    probability = float(
        ckd_model.predict_proba(
            patient_scaled
        )[0][1]
    )

    # --------------------------------------------------------
    # Disease label
    # --------------------------------------------------------

    disease = (
        "No CKD"
        if prediction == 0
        else "Chronic Kidney Disease"
    )

    confidence = round(
        probability * 100,
        2
    )

    return {
        "prediction_class": prediction,
        "prediction": disease,
        "probability": confidence
    }


# ============================================================
# STROKE PREDICTION
# ============================================================

def predict_stroke(patient_data):

    # --------------------------------------------------------
    # Create raw patient DataFrame
    # --------------------------------------------------------

    patient = pd.DataFrame(
        [patient_data],
        columns=STROKE_FEATURES
    )

    # --------------------------------------------------------
    # Numerical columns
    # --------------------------------------------------------

    numerical_columns = [
        "age",
        "hypertension",
        "heart_disease",
        "avg_glucose_level",
        "bmi"
    ]

    # --------------------------------------------------------
    # Convert numerical values
    # --------------------------------------------------------

    for column in numerical_columns:

        patient[column] = pd.to_numeric(
            patient[column],
            errors="coerce"
        )

    # --------------------------------------------------------
    # Impute numerical values
    # --------------------------------------------------------

    patient[numerical_columns] = (
        stroke_imputer.transform(
            patient[numerical_columns]
        )
    )

    # --------------------------------------------------------
    # Categorical columns
    # --------------------------------------------------------

    categorical_columns = [
        "gender",
        "ever_married",
        "work_type",
        "Residence_type",
        "smoking_status"
    ]

    # --------------------------------------------------------
    # One-hot encoding
    # --------------------------------------------------------

    patient_encoded = pd.get_dummies(
        patient,
        columns=categorical_columns,
        drop_first=False
    )

    # --------------------------------------------------------
    # Match exact training features
    # --------------------------------------------------------

    patient_encoded = patient_encoded.reindex(
        columns=stroke_feature_names,
        fill_value=0
    )

    # Ensure exact feature order
    patient_encoded = patient_encoded[
        stroke_feature_names
    ]

    # --------------------------------------------------------
    # Standard scaling
    # --------------------------------------------------------

    patient_scaled = stroke_scaler.transform(
        patient_encoded
    )

    # --------------------------------------------------------
    # Stroke probability
    # --------------------------------------------------------

    probability = float(
        stroke_model.predict_proba(
            patient_scaled
        )[0][1]
    )

    # --------------------------------------------------------
    # Apply selected threshold
    # --------------------------------------------------------

    prediction = int(
        probability >= stroke_threshold
    )

    # --------------------------------------------------------
    # Disease label
    # --------------------------------------------------------

    disease = (
        "No Stroke"
        if prediction == 0
        else "Stroke"
    )

    confidence = round(
        probability * 100,
        2
    )

    return {
        "prediction_class": prediction,
        "prediction": disease,
        "probability": confidence
    }


# ============================================================
# GENERAL PREDICTION
# ============================================================

def predict(patient_data, disease="heart"):

    if disease == "diabetes":

        return predict_diabetes(
            patient_data
        )

    elif disease == "ckd":

        return predict_ckd(
            patient_data
        )

    elif disease == "stroke":

        return predict_stroke(
            patient_data
        )

    # Default: Heart Disease
    return predict_heart(
        patient_data
    )
