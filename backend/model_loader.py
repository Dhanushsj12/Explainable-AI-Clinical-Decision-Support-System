import joblib
import os

# ==========================================
# Base Model Directory
# ==========================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

MODEL_DIR = os.path.join(BASE_DIR, "models")


# ==========================================
# Heart Disease Model
# ==========================================

HEART_MODEL_PATH = os.path.join(
    MODEL_DIR,
    "best_model.pkl"
)

HEART_SCALER_PATH = os.path.join(
    MODEL_DIR,
    "scaler.pkl"
)

heart_model = joblib.load(HEART_MODEL_PATH)
heart_scaler = joblib.load(HEART_SCALER_PATH)


# ==========================================
# Diabetes Model
# ==========================================

DIABETES_MODEL_PATH = os.path.join(
    MODEL_DIR,
    "diabetes",
    "best_model.pkl"
)

DIABETES_SCALER_PATH = os.path.join(
    MODEL_DIR,
    "diabetes_scaler.pkl"
)

diabetes_model = joblib.load(DIABETES_MODEL_PATH)
diabetes_scaler = joblib.load(DIABETES_SCALER_PATH)


# ==========================================
# Default Model
# ==========================================

# Keep these for backward compatibility
# with the existing Heart Disease code.

model = heart_model
scaler = heart_scaler


print("Heart Disease Model Loaded Successfully")
print("Diabetes Model Loaded Successfully")