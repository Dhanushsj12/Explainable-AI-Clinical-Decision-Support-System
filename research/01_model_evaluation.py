"""
01_model_evaluation.py

Research-only evaluation of the four production clinical models
on HELD-OUT REAL test data.

This file does NOT modify the production application.
"""

from pathlib import Path
import sys
import warnings

import numpy as np
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)

warnings.filterwarnings("ignore")


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"

sys.path.insert(0, str(BACKEND))


# ============================================================
# IMPORT PRODUCTION MODELS
# ============================================================

from model_loader import (
    heart_model,
    heart_scaler,
    diabetes_model,
    diabetes_scaler,
    ckd_model,
    ckd_scaler,
    stroke_model,
    stroke_scaler,
    stroke_imputer,
    stroke_feature_names,
    stroke_threshold,
)


# ============================================================
# DATASETS
# ============================================================

DATASETS = {
    "heart": ROOT / "datasets/augmented/heart/heart_test_real.csv",
    "diabetes": ROOT / "datasets/augmented/diabetes/diabetes_test_real.csv",
    "ckd": ROOT / "datasets/augmented/ckd/ckd_test_real.csv",
    "stroke": ROOT / "datasets/augmented/stroke/stroke_test_real.csv",
}


# ============================================================
# FEATURE DEFINITIONS
# ============================================================

HEART_FEATURES = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal",
]

# These will be detected from the existing datasets where possible.
TARGET_CANDIDATES = [
    "target",
    "Target",
    "label",
    "Label",
    "outcome",
    "Outcome",
    "stroke",
    "diabetes",
    "heart_disease",
    "class",
]


# ============================================================
# HELPERS
# ============================================================

def find_target_column(df: pd.DataFrame) -> str:
    for col in TARGET_CANDIDATES:
        if col in df.columns:
            return col

    raise ValueError(
        f"Could not identify target column. "
        f"Available columns: {list(df.columns)}"
    )


def clean_binary_target(series: pd.Series) -> np.ndarray:
    values = series.copy()

    if values.dtype == object:
        mapping = {
            "yes": 1,
            "no": 0,
            "positive": 1,
            "negative": 0,
            "disease": 1,
            "no disease": 0,
            "stroke": 1,
            "no stroke": 0,
            "diabetes": 1,
            "no diabetes": 0,
            "ckd": 1,
            "no ckd": 0,
        }

        values = (
            values.astype(str)
            .str.strip()
            .str.lower()
            .map(lambda x: mapping.get(x, x))
        )

    return pd.to_numeric(values, errors="coerce").fillna(0).astype(int).to_numpy()


# ============================================================
# GENERIC METRICS
# ============================================================

def calculate_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: np.ndarray,
    disease: str,
) -> dict:

    tn, fp, fn, tp = confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1],
    ).ravel()

    specificity = (
        tn / (tn + fp)
        if (tn + fp) > 0
        else 0.0
    )

    try:
        roc_auc = roc_auc_score(
            y_true,
            y_prob,
        )
    except ValueError:
        roc_auc = np.nan

    return {
        "Disease": disease,
        "Samples": len(y_true),
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(
            y_true,
            y_pred,
            zero_division=0,
        ),
        "Recall_Sensitivity": recall_score(
            y_true,
            y_pred,
            zero_division=0,
        ),
        "Specificity": specificity,
        "F1": f1_score(
            y_true,
            y_pred,
            zero_division=0,
        ),
        "ROC_AUC": roc_auc,
        "TN": tn,
        "FP": fp,
        "FN": fn,
        "TP": tp,
    }


# ============================================================
# HEART
# ============================================================

def evaluate_heart() -> dict:

    df = pd.read_csv(DATASETS["heart"])

    target_col = find_target_column(df)

    feature_columns = [
        col for col in HEART_FEATURES
        if col in df.columns
    ]

    X = df[feature_columns].copy()
    y = clean_binary_target(df[target_col])

    X = X.apply(pd.to_numeric, errors="coerce")

    X = X.fillna(X.median())

    X_scaled = heart_scaler.transform(X)

    y_pred = heart_model.predict(X_scaled)

    probabilities = heart_model.predict_proba(
        X_scaled
    )

    y_prob = probabilities[:, 1]

    return calculate_metrics(
        y,
        y_pred,
        y_prob,
        "Heart Disease",
    )


# ============================================================
# DIABETES
# ============================================================

def evaluate_diabetes() -> dict:

    df = pd.read_csv(DATASETS["diabetes"])

    target_col = find_target_column(df)

    X = df.drop(columns=[target_col]).copy()
    y = clean_binary_target(df[target_col])

    # Remove bookkeeping column if present.
    for col in ["data_source", "Unnamed: 0"]:
        if col in X.columns:
            X = X.drop(columns=[col])

    X = X.apply(pd.to_numeric, errors="coerce")
    X = X.fillna(X.median())

    X_scaled = diabetes_scaler.transform(X)

    y_pred = diabetes_model.predict(X_scaled)

    probabilities = diabetes_model.predict_proba(
        X_scaled
    )

    y_prob = probabilities[:, 1]

    return calculate_metrics(
        y,
        y_pred,
        y_prob,
        "Diabetes",
    )


# ============================================================
# CKD
# ============================================================

def evaluate_ckd() -> dict:

    df = pd.read_csv(DATASETS["ckd"])

    target_col = find_target_column(df)

    X = df.drop(columns=[target_col]).copy()
    y = clean_binary_target(df[target_col])

    for col in ["data_source", "Unnamed: 0"]:
        if col in X.columns:
            X = X.drop(columns=[col])

    X = X.apply(pd.to_numeric, errors="coerce")
    X = X.fillna(X.median())

    X_scaled = ckd_scaler.transform(X)

    y_pred = ckd_model.predict(X_scaled)

    probabilities = ckd_model.predict_proba(
        X_scaled
    )

    y_prob = probabilities[:, 1]

    return calculate_metrics(
        y,
        y_pred,
        y_prob,
        "Chronic Kidney Disease",
    )


# ============================================================
# STROKE
# ============================================================


# ============================================================
# STROKE
# ============================================================

def evaluate_stroke() -> dict:
    df = pd.read_csv(DATASETS["stroke"])

    target_col = find_target_column(df)

    if target_col is None:
        raise ValueError(
            "Could not determine Stroke target column."
        )

    # Stroke test data is already preprocessed:
    # one-hot encoded + standardized.
    # Use the exact feature names/order expected by the model.
    missing = [
        col
        for col in stroke_feature_names
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Stroke test data is missing model features: {missing}"
        )

    X = df[stroke_feature_names].copy()

    # Ensure numeric values
    X = X.apply(
        pd.to_numeric,
        errors="coerce"
    )

    # Target conversion
    y = clean_binary_target(
        df[target_col]
    )

    # clean_binary_target returns a NumPy array
    y_array = np.asarray(y)

    valid_mask = ~pd.isna(y_array)

    X = X.loc[valid_mask]
    y_array = y_array[valid_mask].astype(int)

    # Predict probabilities
    probabilities = stroke_model.predict_proba(X)

    y_prob = probabilities[:, 1]

    # Use production Stroke threshold
    y_pred = (
        y_prob >= stroke_threshold
    ).astype(int)

    return calculate_metrics(
        y_array,
        y_pred,
        y_prob,
        "Stroke"
    )


# ==============================
# MAIN
# ==============================


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("XAI-CDSS RESEARCH MODEL EVALUATION")
    print("=" * 70)

    results = []

    evaluators = [
        evaluate_heart,
        evaluate_diabetes,
        evaluate_ckd,
        evaluate_stroke,
    ]

    for evaluator in evaluators:

        disease_name = evaluator.__name__

        print(f"\nRunning: {disease_name}")

        try:
            result = evaluator()

            results.append(result)

            print(
                f"Accuracy:    {result['Accuracy']:.4f}"
            )
            print(
                f"Precision:   {result['Precision']:.4f}"
            )
            print(
                f"Recall:      {result['Recall_Sensitivity']:.4f}"
            )
            print(
                f"Specificity: {result['Specificity']:.4f}"
            )
            print(
                f"F1:          {result['F1']:.4f}"
            )
            print(
                f"ROC-AUC:     {result['ROC_AUC']:.4f}"
            )

        except Exception as exc:

            print(
                f"FAILED: {type(exc).__name__}: {exc}"
            )

    if not results:
        raise RuntimeError(
            "No model evaluation completed."
        )

    results_df = pd.DataFrame(results)

    output_file = (
        ROOT
        / "research"
        / "results"
        / "model_evaluation.csv"
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    results_df.to_csv(
        output_file,
        index=False,
    )

    print("\n" + "=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)

    print(
        results_df.to_string(
            index=False
        )
    )

    print(
        f"\nSaved to:\n{output_file}"
    )


if __name__ == "__main__":
    main()