
"""
05_finalize_research_tables.py

FAST research-result finalizer.

Reads existing CSV results only.
Does NOT retrain models.
Does NOT execute SHAP, LIME, or counterfactual generation.

Run from project root:
    python research\05_finalize_research_tables.py
"""

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "research" / "results"


def read_csv(name: str) -> pd.DataFrame:
    path = RESULTS / name
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return pd.read_csv(path)


def lower_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Case-insensitive column handling without changing values."""
    out = df.copy()
    out.columns = [str(c).strip().lower() for c in out.columns]
    return out


def first_existing(df: pd.DataFrame, *names: str):
    for name in names:
        key = name.strip().lower()
        if key in df.columns:
            return key
    return None


def disease_key(value: str) -> str:
    s = str(value).strip().lower()
    aliases = {
        "heart": "heart",
        "heart disease": "heart",
        "heart_disease": "heart",
        "diabetes": "diabetes",
        "ckd": "ckd",
        "chronic kidney disease": "ckd",
        "chronic_kidney_disease": "ckd",
        "stroke": "stroke",
    }
    return aliases.get(s, s)


def numeric_series(df: pd.DataFrame, col: str):
    if col not in df.columns:
        return pd.Series(dtype=float)
    return pd.to_numeric(df[col], errors="coerce")


def metric_stats(df: pd.DataFrame, col: str):
    vals = numeric_series(df, col).dropna()
    if len(vals) == 0:
        return None
    return {
        "n": int(len(vals)),
        "mean": float(vals.mean()),
        "std": float(vals.std(ddof=1)) if len(vals) > 1 else 0.0,
        "median": float(vals.median()),
        "iqr": float(vals.quantile(0.75) - vals.quantile(0.25)),
    }


def main():
    print("=" * 72)
    print("XAI-CDSS RESEARCH TABLE FINALIZATION")
    print("=" * 72)
    print("Existing CSVs only. No model execution.\n")

    # --------------------------------------------------------------
    # Load existing outputs
    # --------------------------------------------------------------
    model = lower_columns(read_csv("model_evaluation.csv"))
    full = lower_columns(read_csv("full_research_summary.csv"))
    stability = lower_columns(
        read_csv("explanation_stability_detailed.csv")
    )

    # --------------------------------------------------------------
    # 1. FINAL MODEL PERFORMANCE
    # --------------------------------------------------------------
    model.to_csv(
        RESULTS / "model_performance_final.csv",
        index=False
    )

    # --------------------------------------------------------------
    # 2. AGREEMENT
    # --------------------------------------------------------------
    agreement_cols = [
        c for c in [
            "disease",
            "patients_evaluated",
            "agreement_valid_cases",
            "mean_feature_agreement_pct",
            "mean_direction_agreement_pct",
            "mean_ranking_agreement_pct",
            "mean_overall_consistency_pct",
        ]
        if c in full.columns
    ]

    agreement = full[agreement_cols].copy()
    agreement.to_csv(
        RESULTS / "agreement_final.csv",
        index=False
    )

    # --------------------------------------------------------------
    # 3. COUNTERFACTUALS
    # --------------------------------------------------------------
    cf_cols = [
        c for c in [
            "disease",
            "patients_evaluated",
            "counterfactual_valid_cases",
            "counterfactual_success_cases",
            "counterfactual_success_rate_pct",
            "mean_cf_count",
            "mean_cf_feature_count",
            "mean_shap_cf_alignment_pct",
            "mean_lime_cf_alignment_pct",
            "mean_common_cf_alignment_pct",
        ]
        if c in full.columns
    ]

    counterfactual = full[cf_cols].copy()
    counterfactual.to_csv(
        RESULTS / "counterfactual_final.csv",
        index=False
    )

    # --------------------------------------------------------------
    # 4. STABILITY STATISTICS
    #
    # Your stability CSV has been produced with capitalized column
    # names in some versions. We lower-case them here so the script
    # handles both versions safely.
    # --------------------------------------------------------------
    stability_disease_col = first_existing(
        stability, "disease", "Disease"
    )

    if stability_disease_col is None:
        raise ValueError(
            "Could not find the disease column in "
            "explanation_stability_detailed.csv. "
            f"Columns found: {list(stability.columns)}"
        )

    metric_map = {
        "SHAP overlap (%)": first_existing(
            stability, "shap_overlap_pct", "shap_overlap"
        ),
        "SHAP Spearman": first_existing(
            stability, "shap_spearman"
        ),
        "SHAP sign consistency (%)": first_existing(
            stability, "shap_sign_consistency_pct",
            "shap_sign"
        ),
        "LIME overlap (%)": first_existing(
            stability, "lime_overlap_pct", "lime_overlap"
        ),
        "LIME Spearman": first_existing(
            stability, "lime_spearman"
        ),
        "LIME sign consistency (%)": first_existing(
            stability, "lime_sign_consistency_pct",
            "lime_sign"
        ),
    }

    stability_rows = []

    for disease in stability[stability_disease_col].dropna().unique():
        sub = stability[
            stability[stability_disease_col] == disease
        ]

        for label, col in metric_map.items():
            if col is None:
                continue

            stats = metric_stats(sub, col)
            if stats is None:
                continue

            stability_rows.append({
                "disease": str(disease),
                "metric": label,
                **stats,
            })

    stability_final = pd.DataFrame(stability_rows)

    stability_final.to_csv(
        RESULTS / "stability_statistics_final.csv",
        index=False
    )

    # --------------------------------------------------------------
    # 5. HEART AUGMENTATION
    # --------------------------------------------------------------
    heart_aug_path = (
        ROOT / "datasets" / "augmented" / "heart" /
        "heart_augmentation_size_comparison.csv"
    )

    if heart_aug_path.exists():
        pd.read_csv(heart_aug_path).to_csv(
            RESULTS / "augmentation_heart_final.csv",
            index=False
        )

    # --------------------------------------------------------------
    # 6. AVAILABLE BASELINE EVIDENCE
    # --------------------------------------------------------------
    heart_baseline_path = (
        ROOT / "datasets" / "augmented" / "heart" /
        "heart_model_comparison.csv"
    )

    if heart_baseline_path.exists():
        baseline = lower_columns(
            pd.read_csv(heart_baseline_path)
        )

        rows = []
        for _, r in baseline.iterrows():
            rows.append({
                "disease": "Heart Disease",
                "metric": r.get("metric", ""),
                "real_only": r.get(
                    "model a - real only", np.nan
                ),
                "real_plus_synthetic": r.get(
                    "model b - real + synthetic", np.nan
                ),
                "improvement": r.get(
                    "improvement", np.nan
                ),
                "evidence_type": "Existing saved experiment",
            })

        pd.DataFrame(rows).to_csv(
            RESULTS / "baseline_available_final.csv",
            index=False
        )

    # --------------------------------------------------------------
    # 7. POST-HOC ABLATION / COMPONENT COVERAGE
    #
    # Important: these configurations do not change classification
    # metrics because SHAP/LIME/agreement/CF are post-hoc analyses.
    # This table therefore reports model performance alongside the
    # explanatory capabilities that are added.
    # --------------------------------------------------------------
    model_lookup = {}

    for _, r in model.iterrows():
        key = disease_key(r.get("disease", ""))
        model_lookup[key] = r

    ablation_rows = []

    for _, r in full.iterrows():
        disease = str(r.get("disease", "")).strip()
        key = disease_key(disease)
        m = model_lookup.get(key)

        base = {
            "disease": disease,
            "accuracy": (
                m.get("accuracy", np.nan)
                if m is not None else np.nan
            ),
            "precision": (
                m.get("precision", np.nan)
                if m is not None else np.nan
            ),
            "recall": (
                m.get("recall_sensitivity", np.nan)
                if m is not None else np.nan
            ),
            "f1": (
                m.get("f1", np.nan)
                if m is not None else np.nan
            ),
            "roc_auc": (
                m.get("roc_auc", np.nan)
                if m is not None else np.nan
            ),
        }

        patients = float(r.get("patients_evaluated", 0) or 0)
        valid = float(r.get("agreement_valid_cases", 0) or 0)
        explanation_coverage = (
            100.0 * valid / patients
            if patients > 0 else np.nan
        )

        configs = [
            (
                "Prediction only",
                np.nan,
                np.nan,
                np.nan,
                np.nan,
            ),
            (
                "Prediction + SHAP",
                explanation_coverage,
                np.nan,
                np.nan,
                np.nan,
            ),
            (
                "Prediction + LIME",
                explanation_coverage,
                np.nan,
                np.nan,
                np.nan,
            ),
            (
                "Prediction + SHAP + LIME",
                np.nan,
                r.get(
                    "mean_feature_agreement_pct",
                    np.nan
                ),
                r.get(
                    "mean_overall_consistency_pct",
                    np.nan
                ),
                np.nan,
            ),
            (
                "Full XAI-CDSS",
                np.nan,
                r.get(
                    "mean_feature_agreement_pct",
                    np.nan
                ),
                r.get(
                    "mean_overall_consistency_pct",
                    np.nan
                ),
                r.get(
                    "counterfactual_success_rate_pct",
                    np.nan
                ),
            ),
        ]

        for (
            config,
            explanation_cov,
            feature_agreement,
            overall_consistency,
            cf_success,
        ) in configs:

            row = dict(base)

            row.update({
                "configuration": config,
                "explanation_coverage_pct": explanation_cov,
                "feature_agreement_pct": feature_agreement,
                "overall_consistency_pct": overall_consistency,
                "counterfactual_success_rate_pct": cf_success,
                "note": (
                    "Post-hoc component analysis. "
                    "Classification metrics are from the same "
                    "held-out production model."
                ),
            })

            ablation_rows.append(row)

    pd.DataFrame(ablation_rows).to_csv(
        RESULTS / "ablation_posthoc_final.csv",
        index=False
    )

    # --------------------------------------------------------------
    # FINAL STATUS
    # --------------------------------------------------------------
    output_files = [
        "model_performance_final.csv",
        "agreement_final.csv",
        "counterfactual_final.csv",
        "stability_statistics_final.csv",
        "augmentation_heart_final.csv",
        "baseline_available_final.csv",
        "ablation_posthoc_final.csv",
    ]

    print("CREATED:")
    for filename in output_files:
        path = RESULTS / filename
        if path.exists():
            print(f"  OK  {path.name}")

    print("\nCOMPLETED")
    print("No models retrained.")
    print("No SHAP/LIME/counterfactual execution performed.")


if __name__ == "__main__":
    main()
