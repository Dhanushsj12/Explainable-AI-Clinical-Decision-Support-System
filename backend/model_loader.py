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


# =========================
# Stroke
# =========================

STROKE_MODEL_DIR = os.path.join(
    MODEL_DIR, "stroke"
)

STROKE_MODEL_PATH = os.path.join(
    STROKE_MODEL_DIR, "best_model.pkl"
)

STROKE_SCALER_PATH = os.path.join(
    STROKE_MODEL_DIR, "scaler.pkl"
)

STROKE_IMPUTER_PATH = os.path.join(
    STROKE_MODEL_DIR, "imputer.pkl"
)

STROKE_FEATURE_NAMES_PATH = os.path.join(
    STROKE_MODEL_DIR, "feature_names.pkl"
)

STROKE_THRESHOLD_PATH = os.path.join(
    STROKE_MODEL_DIR, "threshold.pkl"
)

stroke_model = joblib.load(STROKE_MODEL_PATH)
stroke_scaler = joblib.load(STROKE_SCALER_PATH)
stroke_imputer = joblib.load(STROKE_IMPUTER_PATH)
stroke_feature_names = joblib.load(STROKE_FEATURE_NAMES_PATH)
stroke_threshold = joblib.load(STROKE_THRESHOLD_PATH)


# =========================
# Backward compatibility
# =========================

model = heart_model
scaler = heart_scaler


# =========================
# Load confirmation
# =========================

print("Heart Disease Model Loaded Successfully")
print("Diabetes Model Loaded Successfully")
print("CKD Model Loaded Successfully")
print("Stroke Model Loaded Successfully")
print(f"Stroke Threshold: {stroke_threshold}")