import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "../models/logistic_regression.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "../models/scaler.pkl")
DATASET_PATH = os.path.join(BASE_DIR, "../datasets/processed/heart_preprocessed.csv")

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
REPORT_FOLDER = os.path.join(BASE_DIR, "reports")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)