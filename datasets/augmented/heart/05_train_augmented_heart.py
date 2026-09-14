import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)


# ============================================================
# PATHS
# ============================================================

TRAIN_FILE = "datasets/augmented/heart/heart_train_augmented.csv"
TEST_FILE = "datasets/augmented/heart/heart_test_real.csv"

OUTPUT_DIR = "models/augmented/heart"

MODEL_FILE = os.path.join(
    OUTPUT_DIR,
    "best_model.pkl"
)

SCALER_FILE = os.path.join(
    OUTPUT_DIR,
    "scaler.pkl"
)

RESULT_FILE = (
    "datasets/augmented/heart/"
    "heart_augmented_model_evaluation.csv"
)


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# LOAD DATA
# ============================================================

train = pd.read_csv(TRAIN_FILE)
test = pd.read_csv(TEST_FILE)


print("\n==========================================")
print("AUGMENTED HEART MODEL TRAINING")
print("==========================================")

print("\nTraining rows :", len(train))
print("Testing rows  :", len(test))


# ============================================================
# REMOVE DATA SOURCE COLUMN
# ============================================================

if "data_source" in train.columns:
    train = train.drop(columns=["data_source"])

if "data_source" in test.columns:
    test = test.drop(columns=["data_source"])


# ============================================================
# SEPARATE FEATURES AND TARGET
# ============================================================

X_train = train.drop(columns=["target"])
y_train = train["target"]

X_test = test.drop(columns=["target"])
y_test = test["target"]


print("\nFeatures:")
print(list(X_train.columns))


# ============================================================
# SCALE DATA
# ============================================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(
    X_train
)

X_test_scaled = scaler.transform(
    X_test
)


# ============================================================
# RANDOM FOREST
# ============================================================

print("\nTraining Random Forest...")

model = RandomForestClassifier(
    random_state=42
)

model.fit(
    X_train_scaled,
    y_train
)


# ============================================================
# PREDICTION
# ============================================================

y_pred = model.predict(
    X_test_scaled
)

y_probability = model.predict_proba(
    X_test_scaled
)


# ============================================================
# METRICS
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    model.predict_proba(X_test)[:, 1]
)


# ============================================================
# RESULTS
# ============================================================

print("\n==========================================")
print("AUGMENTED MODEL RESULTS")
print("==========================================")

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC-AUC   : {roc_auc:.4f}")


# ============================================================
# SAVE MODEL
# ============================================================

joblib.dump(
    model,
    MODEL_FILE
)

joblib.dump(
    scaler,
    SCALER_FILE
)


# ============================================================
# SAVE EVALUATION
# ============================================================

results = pd.DataFrame([
    {
        "model": "Random Forest - Augmented",
        "training_rows": len(train),
        "testing_rows": len(test),
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "roc_auc": roc_auc
    }
])

results.to_csv(
    RESULT_FILE,
    index=False
)


# ============================================================
# COMPLETE
# ============================================================

print("\nSaved:")
print(MODEL_FILE)
print(SCALER_FILE)
print(RESULT_FILE)

print("\nAUGMENTED MODEL TRAINING COMPLETE")