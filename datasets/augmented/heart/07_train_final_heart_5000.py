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
    roc_auc_score,
    confusion_matrix
)


# ============================================================
# PATHS
# ============================================================

TRAIN_REAL_FILE = (
    "datasets/augmented/heart/heart_train_real.csv"
)

TEST_REAL_FILE = (
    "datasets/augmented/heart/heart_test_real.csv"
)

SYNTHETIC_FILE = (
    "datasets/augmented/heart/heart_train_synthetic.csv"
)

MODEL_DIR = (
    "models/augmented/heart"
)

MODEL_FILE = os.path.join(
    MODEL_DIR,
    "best_model.pkl"
)

SCALER_FILE = os.path.join(
    MODEL_DIR,
    "scaler.pkl"
)

EVALUATION_FILE = (
    "datasets/augmented/heart/"
    "heart_final_5000_evaluation.csv"
)


# ============================================================
# CONFIGURATION
# ============================================================

TARGET = "target"

SYNTHETIC_ROWS = 5000

RANDOM_STATE = 42


# ============================================================
# HEADER
# ============================================================

print("\n==========================================")
print("FINAL HEART MODEL - 5,000 SYNTHETIC ROWS")
print("==========================================")


# ============================================================
# LOAD DATA
# ============================================================

train_real = pd.read_csv(
    TRAIN_REAL_FILE
)

test_real = pd.read_csv(
    TEST_REAL_FILE
)

synthetic_data = pd.read_csv(
    SYNTHETIC_FILE
)


# ============================================================
# REMOVE DATA SOURCE COLUMN
# ============================================================

if "data_source" in train_real.columns:

    train_real = train_real.drop(
        columns=["data_source"]
    )

    print(
        "Removed data_source from real training data."
    )


if "data_source" in test_real.columns:

    test_real = test_real.drop(
        columns=["data_source"]
    )

    print(
        "Removed data_source from real testing data."
    )


if "data_source" in synthetic_data.columns:

    synthetic_data = synthetic_data.drop(
        columns=["data_source"]
    )

    print(
        "Removed data_source from synthetic data."
    )


# ============================================================
# USE EXACTLY 5,000 SYNTHETIC ROWS
# ============================================================

if len(synthetic_data) < SYNTHETIC_ROWS:

    raise ValueError(
        "Synthetic dataset contains fewer than "
        "5,000 rows."
    )


synthetic_data = synthetic_data.sample(
    n=SYNTHETIC_ROWS,
    random_state=RANDOM_STATE
).reset_index(drop=True)


# ============================================================
# DISPLAY DATASET SIZES
# ============================================================

print("\nDATASET SIZES")
print("-------------")

print(
    "Real training rows      :",
    len(train_real)
)

print(
    "Synthetic training rows :",
    len(synthetic_data)
)

print(
    "Final training rows     :",
    len(train_real) + len(synthetic_data)
)

print(
    "Real testing rows       :",
    len(test_real)
)


# ============================================================
# TARGET CLASSES
# ============================================================

print("\nTARGET CLASSES")
print("-------------")

print(
    "Real training      :",
    sorted(train_real[TARGET].unique())
)

print(
    "Synthetic          :",
    sorted(synthetic_data[TARGET].unique())
)

print(
    "Real testing       :",
    sorted(test_real[TARGET].unique())
)


# ============================================================
# TARGET DISTRIBUTION
# ============================================================

print("\nREAL TRAINING TARGET DISTRIBUTION")
print("---------------------------------")

print(
    train_real[TARGET]
    .value_counts()
    .sort_index()
)


print("\nSYNTHETIC TARGET DISTRIBUTION")
print("-----------------------------")

print(
    synthetic_data[TARGET]
    .value_counts()
    .sort_index()
)


# ============================================================
# FEATURES
# ============================================================

FEATURES = [
    column
    for column in train_real.columns
    if column != TARGET
]


print("\nFEATURES")
print("--------")

print(FEATURES)


# ============================================================
# PREPARE TRAINING DATA
# ============================================================

X_train_real = train_real[
    FEATURES
]

y_train_real = train_real[
    TARGET
]


X_train_synthetic = synthetic_data[
    FEATURES
]

y_train_synthetic = synthetic_data[
    TARGET
]


# ============================================================
# COMBINE REAL + SYNTHETIC
# ============================================================

X_train = pd.concat(
    [
        X_train_real,
        X_train_synthetic
    ],
    ignore_index=True
)

y_train = pd.concat(
    [
        y_train_real,
        y_train_synthetic
    ],
    ignore_index=True
)


# ============================================================
# REAL TEST SET ONLY
# ============================================================

X_test = test_real[
    FEATURES
]

y_test = test_real[
    TARGET
]


print("\nTEST SET")
print("--------")

print(
    "Test rows:",
    len(X_test)
)

print("\nTest target distribution:")

print(
    y_test.value_counts()
    .sort_index()
)


print("\nIMPORTANT:")
print(
    "The test set contains ONLY real data."
)

print(
    "The test set was NOT used for augmentation."
)

print(
    "The same 61 real test rows are used for evaluation."
)


# ============================================================
# SCALE FEATURES
# ============================================================

print("\n==========================================")
print("FEATURE SCALING")
print("==========================================")

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(
    X_train
)

X_test_scaled = scaler.transform(
    X_test
)


# ============================================================
# TRAIN RANDOM FOREST
# ============================================================

print("\n==========================================")
print("TRAINING FINAL 5K AUGMENTED MODEL")
print("==========================================")

print(
    "Training rows:",
    len(X_train)
)

print(
    "Real rows:",
    len(X_train_real)
)

print(
    "Synthetic rows:",
    len(X_train_synthetic)
)

print("\nTraining Random Forest...")


model = RandomForestClassifier(
    n_estimators=300,
    random_state=RANDOM_STATE,
    class_weight="balanced",
    n_jobs=-1
)


model.fit(
    X_train_scaled,
    y_train
)


# ============================================================
# PREDICTION
# ============================================================

prediction = model.predict(
    X_test_scaled
)

probability = model.predict_proba(
    X_test_scaled
)


# ============================================================
# METRICS
# ============================================================

accuracy = accuracy_score(
    y_test,
    prediction
)

precision = precision_score(
    y_test,
    prediction,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    y_test,
    prediction,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    y_test,
    prediction,
    average="weighted",
    zero_division=0
)


# ============================================================
# ROC-AUC
# ============================================================

try:

    auc = roc_auc_score(
        y_test,
        probability[:, 1]
    )

except ValueError:

    auc = float("nan")


# ============================================================
# CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_test,
    prediction
)


# ============================================================
# RESULTS
# ============================================================

print("\n==========================================")
print("FINAL 5K AUGMENTED MODEL RESULTS")
print("==========================================")

print(
    f"Accuracy  : {accuracy:.4f}"
)

print(
    f"Precision : {precision:.4f}"
)

print(
    f"Recall    : {recall:.4f}"
)

print(
    f"F1 Score  : {f1:.4f}"
)

print(
    f"ROC-AUC   : {auc:.4f}"
)


print("\nConfusion Matrix:")

print(cm)


# ============================================================
# SAVE MODEL DIRECTORY
# ============================================================

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


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

evaluation = pd.DataFrame({

    "training_real_rows": [
        len(train_real)
    ],

    "training_synthetic_rows": [
        len(synthetic_data)
    ],

    "training_total_rows": [
        len(X_train)
    ],

    "testing_real_rows": [
        len(test_real)
    ],

    "accuracy": [
        accuracy
    ],

    "precision": [
        precision
    ],

    "recall": [
        recall
    ],

    "f1_score": [
        f1
    ],

    "roc_auc": [
        auc
    ]

})


evaluation.to_csv(
    EVALUATION_FILE,
    index=False
)


# ============================================================
# FINAL INFORMATION
# ============================================================

print("\n==========================================")
print("FILES SAVED")
print("==========================================")

print(
    "Model :",
    MODEL_FILE
)

print(
    "Scaler:",
    SCALER_FILE
)

print(
    "Evaluation:",
    EVALUATION_FILE
)


print("\n==========================================")
print("FINAL 5K HEART MODEL TRAINING COMPLETE")
print("==========================================")