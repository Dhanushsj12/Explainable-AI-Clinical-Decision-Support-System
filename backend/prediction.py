import numpy as np
from model_loader import model, scaler

def predict(patient_data):

    patient = np.array(patient_data).reshape(1, -1)

    patient = scaler.transform(patient)

    prediction = int(model.predict(patient)[0])

    probability = float(model.predict_proba(patient)[0][1])

    if prediction == 0:
        disease = "No Heart Disease"
    else:
        disease = "Heart Disease"

    confidence = round(probability * 100, 2)

    return {
        "prediction_class": prediction,
        "prediction": disease,
        "probability": confidence
    }