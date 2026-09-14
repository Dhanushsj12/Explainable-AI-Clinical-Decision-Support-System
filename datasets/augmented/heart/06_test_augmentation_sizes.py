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

SYNTHETIC_FILE = (
    "datasets/augmented/heart/heart_train_synthetic.csv"
)

RESULT_FILE = (
    "datasets/augmented/heart/heart_augmentation_size_comparison.csv"
)


# ============================================================
# CONFIGURATION
# ============================================================

SYNTHETIC_SIZES = [
    500,
    1000,
    2000,
    5000
]

TARGET = "target"

RANDOM_STATE = 42


# ============================================================
# LOAD DATA
# ============================================================

print("\n==========================================")
print("HEART DISEASE AUGMENTATION SIZE EXPERIMENT")
print("==========================================")

train_real = pd.read_csv(TRAIN_REAL_FILE)
test_real = pd.read_csv(TEST_REAL_FILE)
synthetic_data = pd.read_csv(SYNTHETIC_FILE)


print("\nDATASET SIZES")
print("-------------")

print("Real training rows :", len(train_real))
print("Real testing rows  :", len(test_real))
print("Synthetic rows      :", len(synthetic_data))


# ============================================================
# REMOVE DATA SOURCE COLUMN
# ============================================================

for dataframe_name, dataframe in [
    ("real training", train_real),
    ("real testing", test_real),
    ("synthetic", synthetic_data)
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
# VERIFY TARGET CLASSES
# ============================================================

print("\nTARGET CLASSES")
print("-------------")

print(
    "Real training      :",
    sorted(train_real[TARGET].unique())
)

print(
    "Real testing       :",
    sorted(test_real[TARGET].unique())
)

print(
    "Synthetic          :",
    sorted(synthetic_data[TARGET].unique())
)


# ============================================================
# VERIFY TEST SET
# ============================================================

X_test = test_real[FEATURES]
y_test = test_real[TARGET]


print("\nTEST SET")
print("--------")

print("Test rows:", len(X_test))

print("\nTest target distribution:")
print(
    y_test.value_counts().sort_index()
)

print("\nIMPORTANT:")
print("The test set contains ONLY REAL data.")
print("The test set is NOT used for augmentation.")
print("Every experiment uses the SAME 61 real test rows.")


# ============================================================
# MODEL A - REAL ONLY
# ============================================================

print("\n==========================================")
print("BASELINE MODEL")
print("==========================================")

X_train_real = train_real[FEATURES]
y_train_real = train_real[TARGET]


baseline_model = RandomForestClassifier(
    n_estimators=300,
    random_state=RANDOM_STATE,
    class_weight="balanced",
    n_jobs=-1
)


baseline_model.fit(
    X_train_real,
    y_train_real
)


baseline_prediction = baseline_model.predict(
    X_test
)

baseline_probability = baseline_model.predict_proba(
    X_test
)[:, 1]


baseline_accuracy = accuracy_score(
    y_test,
    baseline_prediction
)

baseline_precision = precision_score(
    y_test,
    baseline_prediction,
    average="binary",
    zero_division=0
)

baseline_recall = recall_score(
    y_test,
    baseline_prediction,
    average="binary",
    zero_division=0
)

baseline_f1 = f1_score(
    y_test,
    baseline_prediction,
    average="binary",
    zero_division=0
)

baseline_auc = roc_auc_score(
    y_test,
    baseline_probability
)


print("\nBASELINE RESULTS")
print("----------------")

print(
    f"Accuracy  : {baseline_accuracy:.4f}"
)

print(
    f"Precision : {baseline_precision:.4f}"
)

print(
    f"Recall    : {baseline_recall:.4f}"
)

print(
    f"F1 Score  : {baseline_f1:.4f}"
)

print(
    f"ROC-AUC   : {baseline_auc:.4f}"
)

print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_test,
        baseline_prediction
    )
)


# ============================================================
# STORE RESULTS
# ============================================================

results = []


results.append({

    "Synthetic Rows": 0,

    "Total Training Rows": len(train_real),

    "Accuracy": baseline_accuracy,

    "Precision": baseline_precision,

    "Recall": baseline_recall,

    "F1 Score": baseline_f1,

    "ROC-AUC": baseline_auc,

    "Accuracy Change": 0.0,

    "Precision Change": 0.0,

    "Recall Change": 0.0,

    "F1 Change": 0.0,

    "ROC-AUC Change": 0.0

})


# ============================================================
# AUGMENTATION EXPERIMENTS
# ============================================================

for synthetic_size in SYNTHETIC_SIZES:

    print("\n==========================================")
    print(
        f"EXPERIMENT: {synthetic_size:,} SYNTHETIC ROWS"
    )
    print("==========================================")

    # --------------------------------------------------------
    # Select synthetic rows
    # --------------------------------------------------------

    synthetic_sample = synthetic_data.sample(
        n=synthetic_size,
        random_state=RANDOM_STATE
    )


    # --------------------------------------------------------
    # Combine real + synthetic
    # --------------------------------------------------------

    augmented_train = pd.concat(
        [
            train_real,
            synthetic_sample
        ],
        ignore_index=True
    )


    print(
        "Real rows      :",
        len(train_real)
    )

    print(
        "Synthetic rows :",
        len(synthetic_sample)
    )

    print(
        "Total rows     :",
        len(augmented_train)
    )


    # --------------------------------------------------------
    # Training data
    # --------------------------------------------------------

    X_train = augmented_train[FEATURES]

    y_train = augmented_train[TARGET]


    # --------------------------------------------------------
    # Model
    # --------------------------------------------------------

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=RANDOM_STATE,
        class_weight="balanced",
        n_jobs=-1
    )


    print("\nTraining Random Forest...")

    model.fit(
        X_train,
        y_train
    )


    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    prediction = model.predict(
        X_test
    )

    probability = model.predict_proba(
        X_test
    )[:, 1]


    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    accuracy = accuracy_score(
        y_test,
        prediction
    )

    precision = precision_score(
        y_test,
        prediction,
        average="binary",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        prediction,
        average="binary",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        prediction,
        average="binary",
        zero_division=0
    )

    auc = roc_auc_score(
        y_test,
        probability
    )


    # --------------------------------------------------------
    # Print results
    # --------------------------------------------------------

    print("\nRESULTS")
    print("-------")

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

    print(
        confusion_matrix(
            y_test,
            prediction
        )
    )


    # --------------------------------------------------------
    # Store results
    # --------------------------------------------------------

    results.append({

        "Synthetic Rows": synthetic_size,

        "Total Training Rows": len(augmented_train),

        "Accuracy": accuracy,

        "Precision": precision,

        "Recall": recall,

        "F1 Score": f1,

        "ROC-AUC": auc,

        "Accuracy Change":
            accuracy - baseline_accuracy,

        "Precision Change":
            precision - baseline_precision,

        "Recall Change":
            recall - baseline_recall,

        "F1 Change":
            f1 - baseline_f1,

        "ROC-AUC Change":
            auc - baseline_auc

    })


# ============================================================
# FINAL COMPARISON
# ============================================================

comparison = pd.DataFrame(
    results
)


print("\n==========================================")
print("FINAL AUGMENTATION COMPARISON")
print("==========================================")


print(
    comparison.to_string(
        index=False
    )
)


# ============================================================
# BEST CONFIGURATION
# ============================================================

print("\n==========================================")
print("BEST CONFIGURATION")
print("==========================================")


best_accuracy_row = comparison.loc[
    comparison["Accuracy"].idxmax()
]

best_f1_row = comparison.loc[
    comparison["F1 Score"].idxmax()
]

best_auc_row = comparison.loc[
    comparison["ROC-AUC"].idxmax()
]


print(
    "\nBest Accuracy:"
)

print(
    f"Synthetic rows = "
    f"{int(best_accuracy_row['Synthetic Rows']):,}"
)

print(
    f"Accuracy = "
    f"{best_accuracy_row['Accuracy']:.4f}"
)


print(
    "\nBest F1 Score:"
)

print(
    f"Synthetic rows = "
    f"{int(best_f1_row['Synthetic Rows']):,}"
)

print(
    f"F1 Score = "
    f"{best_f1_row['F1 Score']:.4f}"
)


print(
    "\nBest ROC-AUC:"
)

print(
    f"Synthetic rows = "
    f"{int(best_auc_row['Synthetic Rows']):,}"
)

print(
    f"ROC-AUC = "
    f"{best_auc_row['ROC-AUC']:.4f}"
)


# ============================================================
# DECISION
# ============================================================

print("\n==========================================")
print("AUGMENTATION DECISION")
print("==========================================")


if (
    best_accuracy_row["Accuracy"]
    > baseline_accuracy
):

    print(
        "At least one augmentation size "
        "improved Accuracy over the real-only baseline."
    )

else:

    print(
        "None of the tested augmentation sizes "
        "improved Accuracy over the real-only baseline."
    )


if (
    best_f1_row["F1 Score"]
    > baseline_f1
):

    print(
        "At least one augmentation size "
        "improved F1 Score."
    )

else:

    print(
        "None of the tested augmentation sizes "
        "improved F1 Score."
    )


if (
    best_auc_row["ROC-AUC"]
    > baseline_auc
):

    print(
        "At least one augmentation size "
        "improved ROC-AUC."
    )

else:

    print(
        "None of the tested augmentation sizes "
        "improved ROC-AUC."
    )


# ============================================================
# SAVE RESULTS
# ============================================================

comparison.to_csv(
    RESULT_FILE,
    index=False
)


print("\nSaved:")

print(
    RESULT_FILE
)


print("\n==========================================")
print("AUGMENTATION SIZE EXPERIMENT COMPLETE")
print("==========================================")