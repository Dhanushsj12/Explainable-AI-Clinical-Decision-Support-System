import numpy as np
import pandas as pd

from model_loader import (
    heart_model,
    heart_scaler,
    diabetes_model,
    diabetes_scaler,
    ckd_model,
    ckd_scaler
)


# =========================
# CKD Feature Names
# =========================

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


# =========================
# Heart Disease Prediction
# =========================

def predict_heart(patient_data):

    patient = np.array(
        patient_data
    ).reshape(1, -1)

    patient_scaled = heart_scaler.transform(
        patient
    )

    prediction = int(
        heart_model.predict(patient_scaled)[0]
    )

    probability = float(
        heart_model.predict_proba(
            patient_scaled
        )[0][1]
    )

    disease = (
        "No Heart Disease"
        if prediction == 0
        else "Heart Disease"
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


# =========================
# Diabetes Prediction
# =========================

def predict_diabetes(patient_data):

    patient = np.array(
        patient_data
    ).reshape(1, -1)

    patient_scaled = diabetes_scaler.transform(
        patient
    )

    prediction = int(
        diabetes_model.predict(patient_scaled)[0]
    )

    probability = float(
        diabetes_model.predict_proba(
            patient_scaled
        )[0][1]
    )

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


# =========================
# CKD Prediction
# =========================

def predict_ckd(patient_data):

    patient = pd.DataFrame(
        [patient_data],
        columns=CKD_FEATURES
    )

    patient_scaled = ckd_scaler.transform(
        patient
    )

    prediction = int(
        ckd_model.predict(patient_scaled)[0]
    )

    probability = float(
        ckd_model.predict_proba(
            patient_scaled
        )[0][1]
    )

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


# =========================
# General Prediction
# =========================

def predict(patient_data, disease="heart"):

    if disease == "diabetes":

        return predict_diabetes(
            patient_data
        )

    elif disease == "ckd":

        return predict_ckd(
            patient_data
        )

    return predict_heart(
        patient_data
    )