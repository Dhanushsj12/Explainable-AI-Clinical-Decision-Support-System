import joblib
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

MODEL_DIR = os.path.join(BASE_DIR, "models")


# =========================
# Heart Disease
# =========================

HEART_MODEL_PATH = os.path.join(
    MODEL_DIR, "best_model.pkl"
)

HEART_SCALER_PATH = os.path.join(
    MODEL_DIR, "scaler.pkl"
)

heart_model = joblib.load(HEART_MODEL_PATH)
heart_scaler = joblib.load(HEART_SCALER_PATH)


# =========================
# Diabetes
# =========================

DIABETES_MODEL_PATH = os.path.join(
    MODEL_DIR, "diabetes", "best_model.pkl"
)

DIABETES_SCALER_PATH = os.path.join(
    MODEL_DIR, "diabetes_scaler.pkl"
)

diabetes_model = joblib.load(DIABETES_MODEL_PATH)
diabetes_scaler = joblib.load(DIABETES_SCALER_PATH)


# =========================
# CKD
# =========================

CKD_MODEL_PATH = os.path.join(
    MODEL_DIR, "ckd", "best_model.pkl"
)

CKD_SCALER_PATH = os.path.join(
    MODEL_DIR, "ckd", "scaler.pkl"
)

ckd_model = joblib.load(CKD_MODEL_PATH)
ckd_scaler = joblib.load(CKD_SCALER_PATH)


# Backward compatibility
model = heart_model
scaler = heart_scaler


print("Heart Disease Model Loaded Successfully")
print("Diabetes Model Loaded Successfully")
print("CKD Model Loaded Successfully")