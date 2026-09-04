import numpy as np

from model_loader import (
    heart_model,
    heart_scaler,
    diabetes_model,
    diabetes_scaler
)


# ==========================================
# Heart Disease Prediction
# ==========================================

def predict_heart(patient_data):

    patient = np.array(patient_data).reshape(1, -1)

    patient_scaled = heart_scaler.transform(patient)

    prediction = int(
        heart_model.predict(patient_scaled)[0]
    )

    probability = float(
        heart_model.predict_proba(patient_scaled)[0][1]
    )

    if prediction == 0:
        disease = "No Heart Disease"
    else:
        disease = "Heart Disease"

    confidence = round(
        probability * 100,
        2
    )

    return {
        "prediction_class": prediction,
        "prediction": disease,
        "probability": confidence
    }


# ==========================================
# Diabetes Prediction
# ==========================================

def predict_diabetes(patient_data):

    patient = np.array(patient_data).reshape(1, -1)

    patient_scaled = diabetes_scaler.transform(patient)

    prediction = int(
        diabetes_model.predict(patient_scaled)[0]
    )

    probability = float(
        diabetes_model.predict_proba(patient_scaled)[0][1]
    )

    if prediction == 0:
        disease = "No Diabetes"
    else:
        disease = "Diabetes"

    confidence = round(
        probability * 100,
        2
    )

    return {
        "prediction_class": prediction,
        "prediction": disease,
        "probability": confidence
    }


# ==========================================
# General Prediction Function
# ==========================================

def predict(patient_data, disease="heart"):

    if disease == "diabetes":
        return predict_diabetes(patient_data)

    return predict_heart(patient_data)