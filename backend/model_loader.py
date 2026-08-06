import joblib

MODEL_PATH = "../models/logistic_regression.pkl"
SCALER_PATH = "../models/scaler.pkl"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

print("Model Loaded Successfully")