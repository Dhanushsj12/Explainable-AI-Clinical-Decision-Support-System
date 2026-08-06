import pandas as pd
import joblib
import shap

# ==========================================
# Load Model and Scaler
# ==========================================

model = joblib.load("../models/logistic_regression.pkl")
scaler = joblib.load("../models/scaler.pkl")

# ==========================================
# Load Dataset
# ==========================================

df = pd.read_csv("../datasets/processed/heart_preprocessed.csv")

X = df.drop("target", axis=1)

# Scale dataset
X_scaled = scaler.transform(X)

# ==========================================
# Feature Labels (User-Friendly Names)
# ==========================================

FEATURE_LABELS = {
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

# ==========================================
# Create SHAP Explainer
# ==========================================

explainer = shap.Explainer(model, X_scaled)

feature_names = list(X.columns)

# ==========================================
# Explain Prediction
# ==========================================

def explain(patient):

    patient_df = pd.DataFrame([patient], columns=feature_names)

    patient_scaled = scaler.transform(patient_df)

    shap_values = explainer(patient_scaled)

    values = shap_values.values[0]

    explanation = []

    for feature, impact in zip(feature_names, values):

        explanation.append({

            "feature": FEATURE_LABELS.get(feature, feature),

            "impact": round(float(impact), 4)

        })

    # Sort by highest absolute impact
    explanation.sort(
        key=lambda x: abs(x["impact"]),
        reverse=True
    )

    # Return Top 5 Features
    return explanation[:5]