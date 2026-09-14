import os
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
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

TRAIN_AUGMENTED_FILE = (
    "datasets/augmented/heart/heart_train_augmented.csv"
)

RESULT_FILE = (
    "datasets/augmented/heart/heart_model_comparison.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("\n==========================================")
print("HEART DISEASE MODEL A/B COMPARISON")
print("==========================================")

train_real = pd.read_csv(TRAIN_REAL_FILE)
test_real = pd.read_csv(TEST_REAL_FILE)
train_augmented = pd.read_csv(TRAIN_AUGMENTED_FILE)


# ============================================================
# DATASET INFORMATION
# ============================================================

print("\nDATASET SIZES")
print("-------------")

print(
    "Real training rows      :",
    len(train_real)
)

print(
    "Real testing rows       :",
    len(test_real)
)

print(
    "Augmented training rows :",
    len(train_augmented)
)


# ============================================================
# REMOVE DATA SOURCE COLUMN
# ============================================================

for dataframe_name, dataframe in [
    ("real training", train_real),
    ("real testing", test_real),
    ("augmented training", train_augmented)
]:

    if "data_source" in dataframe.columns:

        dataframe.drop(
            columns=["data_source"],
            inplace=True
        )

        print(
            f"Removed data_source from {dataframe_name} data."
        )


# ============================================================
# TARGET
# ============================================================

TARGET = "target"


# ============================================================
# CHECK TARGET EXISTS
# ============================================================

if TARGET not in train_real.columns:

    raise ValueError(
        "ERROR: 'target' column not found in real training data."
    )

if TARGET not in test_real.columns:

    raise ValueError(
        "ERROR: 'target' column not found in real testing data."
    )

if TARGET not in train_augmented.columns:

    raise ValueError(
        "ERROR: 'target' column not found in augmented training data."
    )


# ============================================================
# CHECK TARGET IS BINARY
# ============================================================

real_train_classes = sorted(
    train_real[TARGET].unique()
)

real_test_classes = sorted(
    test_real[TARGET].unique()
)

augmented_classes = sorted(
    train_augmented[TARGET].unique()
)


print("\nTARGET CLASSES")
print("-------------")

print(
    "Real training      :",
    real_train_classes
)

print(
    "Real testing       :",
    real_test_classes
)

print(
    "Augmented training :",
    augmented_classes
)


if not set(real_train_classes).issubset({0, 1}):

    raise ValueError(
        f"""
ERROR: Real training target is not binary.

Found:
{real_train_classes}

Expected:
[0, 1]
"""
    )


if not set(real_test_classes).issubset({0, 1}):

    raise ValueError(
        f"""
ERROR: Real testing target is not binary.

Found:
{real_test_classes}

Expected:
[0, 1]
"""
    )


if not set(augmented_classes).issubset({0, 1}):

    raise ValueError(
        f"""
ERROR: Augmented training target is not binary.

Found:
{augmented_classes}

Expected:
[0, 1]
"""
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


print("\nREAL TESTING TARGET DISTRIBUTION")
print("--------------------------------")

print(
    test_real[TARGET]
    .value_counts()
    .sort_index()
)


print("\nAUGMENTED TRAINING TARGET DISTRIBUTION")
print("---------------------------------------")

print(
    train_augmented[TARGET]
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
# CREATE TRAINING AND TESTING DATA
# ============================================================

X_train_real = train_real[FEATURES]
y_train_real = train_real[TARGET]

X_test_real = test_real[FEATURES]
y_test_real = test_real[TARGET]

X_train_augmented = train_augmented[FEATURES]
y_train_augmented = train_augmented[TARGET]


print("\nTEST SET")
print("--------")

print(
    "Test rows:",
    len(X_test_real)
)

print("\nIMPORTANT:")
print("The test set contains ONLY REAL data.")
print("The test set is NOT used during augmentation.")
print("Both models are evaluated on exactly the SAME test set.")


# ============================================================
# MODEL A
# REAL TRAINING DATA ONLY
# ============================================================

print("\n==========================================")
print("MODEL A")
print("==========================================")

print(
    "Training using REAL training data only..."
)


model_a = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)


model_a.fit(
    X_train_real,
    y_train_real
)


prediction_a = model_a.predict(
    X_test_real
)


probability_a = model_a.predict_proba(
    X_test_real
)[:, 1]


# ============================================================
# MODEL A METRICS
# ============================================================

accuracy_a = accuracy_score(
    y_test_real,
    prediction_a
)


precision_a = precision_score(
    y_test_real,
    prediction_a,
    zero_division=0
)


recall_a = recall_score(
    y_test_real,
    prediction_a,
    zero_division=0
)


f1_a = f1_score(
    y_test_real,
    prediction_a,
    zero_division=0
)


auc_a = roc_auc_score(
    y_test_real,
    probability_a
)


cm_a = confusion_matrix(
    y_test_real,
    prediction_a
)


print("\nMODEL A RESULTS")
print("----------------")

print(
    f"Accuracy  : {accuracy_a:.4f}"
)

print(
    f"Precision : {precision_a:.4f}"
)

print(
    f"Recall    : {recall_a:.4f}"
)

print(
    f"F1 Score  : {f1_a:.4f}"
)

print(
    f"ROC-AUC   : {auc_a:.4f}"
)

print("\nConfusion Matrix:")

print(cm_a)


# ============================================================
# MODEL B
# REAL + SYNTHETIC TRAINING DATA
# ============================================================

print("\n==========================================")
print("MODEL B")
print("==========================================")

print(
    "Training using REAL + SYNTHETIC data..."
)


model_b = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)


model_b.fit(
    X_train_augmented,
    y_train_augmented
)


prediction_b = model_b.predict(
    X_test_real
)


probability_b = model_b.predict_proba(
    X_test_real
)[:, 1]


# ============================================================
# MODEL B METRICS
# ============================================================

accuracy_b = accuracy_score(
    y_test_real,
    prediction_b
)


precision_b = precision_score(
    y_test_real,
    prediction_b,
    zero_division=0
)


recall_b = recall_score(
    y_test_real,
    prediction_b,
    zero_division=0
)


f1_b = f1_score(
    y_test_real,
    prediction_b,
    zero_division=0
)


auc_b = roc_auc_score(
    y_test_real,
    probability_b
)


cm_b = confusion_matrix(
    y_test_real,
    prediction_b
)


print("\nMODEL B RESULTS")
print("----------------")

print(
    f"Accuracy  : {accuracy_b:.4f}"
)

print(
    f"Precision : {precision_b:.4f}"
)

print(
    f"Recall    : {recall_b:.4f}"
)

print(
    f"F1 Score  : {f1_b:.4f}"
)

print(
    f"ROC-AUC   : {auc_b:.4f}"
)

print("\nConfusion Matrix:")

print(cm_b)


# ============================================================
# COMPARISON
# ============================================================

accuracy_improvement = (
    accuracy_b - accuracy_a
)

precision_improvement = (
    precision_b - precision_a
)

recall_improvement = (
    recall_b - recall_a
)

f1_improvement = (
    f1_b - f1_a
)

auc_improvement = (
    auc_b - auc_a
)


# ============================================================
# FINAL COMPARISON TABLE
# ============================================================

comparison = pd.DataFrame({

    "Metric": [
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "ROC-AUC"
    ],

    "Model A - Real Only": [
        accuracy_a,
        precision_a,
        recall_a,
        f1_a,
        auc_a
    ],

    "Model B - Real + Synthetic": [
        accuracy_b,
        precision_b,
        recall_b,
        f1_b,
        auc_b
    ],

    "Improvement": [
        accuracy_improvement,
        precision_improvement,
        recall_improvement,
        f1_improvement,
        auc_improvement
    ]
})


print("\n==========================================")
print("FINAL COMPARISON")
print("==========================================")


print(
    comparison.to_string(
        index=False
    )
)


# ============================================================
# AUGMENTATION DECISION
# ============================================================

print("\n==========================================")
print("AUGMENTATION DECISION")
print("==========================================")


if accuracy_b > accuracy_a:

    print(
        "MODEL B improved Accuracy over Model A."
    )

elif accuracy_b < accuracy_a:

    print(
        "MODEL B did NOT improve Accuracy."
    )

else:

    print(
        "MODEL B has the SAME Accuracy as Model A."
    )


print("\nMetric-wise decision:")


if precision_b > precision_a:

    print("Precision : IMPROVED")

elif precision_b < precision_a:

    print("Precision : DECREASED")

else:

    print("Precision : SAME")


if recall_b > recall_a:

    print("Recall    : IMPROVED")

elif recall_b < recall_a:

    print("Recall    : DECREASED")

else:

    print("Recall    : SAME")


if f1_b > f1_a:

    print("F1 Score  : IMPROVED")

elif f1_b < f1_a:

    print("F1 Score  : DECREASED")

else:

    print("F1 Score  : SAME")


if auc_b > auc_a:

    print("ROC-AUC   : IMPROVED")

elif auc_b < auc_a:

    print("ROC-AUC   : DECREASED")

else:

    print("ROC-AUC   : SAME")


# ============================================================
# SAVE COMPARISON
# ============================================================

comparison.to_csv(
    RESULT_FILE,
    index=False
)


print("\nSaved:")
print(RESULT_FILE)


# ============================================================
# COMPLETE
# ============================================================

print("\n==========================================")
print("COMPARISON COMPLETE")
print("==========================================")