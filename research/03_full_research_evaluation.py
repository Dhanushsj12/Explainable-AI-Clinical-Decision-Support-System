"""
03_full_research_evaluation.py

Research-only evaluation runner for XAI-CDSS.
It does NOT modify backend/frontend/model files.

Runs:
1) Dataset-level SHAP-LIME agreement on real test data.
2) Counterfactual evaluation on sampled real test patients.
3) Explanation-counterfactual alignment.
4) Baseline comparison using model outputs already reported in the project,
   where available, without retraining production models.
5) Ablation study over explanation components using the same patient set.
6) Exports CSV tables for paper preparation.

Run from project root:
    python research\03_full_research_evaluation.py
"""

from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

# Make backend importable without changing project code.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from model_loader import stroke_threshold  # type: ignore
from explainability import explain  # type: ignore
from lime_explain import lime_explain  # type: ignore
from shap_lime_agreement import calculate_shap_lime_agreement  # type: ignore
from counterfactual_heart import find_counterfactuals  # type: ignore


RESULTS_DIR = PROJECT_ROOT / "research" / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42
rng = np.random.default_rng(RANDOM_SEED)
TOP_K = 5
PATIENTS_PER_DISEASE = 25
MAX_CF_RESULTS = 5

TEST_FILES = {
    "heart": PROJECT_ROOT / "datasets/augmented/heart/heart_test_real.csv",
    "diabetes": PROJECT_ROOT / "datasets/augmented/diabetes/diabetes_test_real.csv",
    "ckd": PROJECT_ROOT / "datasets/augmented/ckd/ckd_test_real.csv",
    "stroke": PROJECT_ROOT / "datasets/augmented/stroke/stroke_test_real.csv",
}

RAW_FEATURES = {
    "heart": ["age","sex","cp","trestbps","chol","fbs","restecg","thalach","exang","oldpeak","slope","ca","thal"],
    "diabetes": ["age","gender","polyuria","polydipsia","sudden_weight_loss","weakness","polyphagia",
                 "genital_thrush","visual_blurring","itching","irritability","delayed_healing",
                 "partial_paresis","muscle_stiffness","alopecia","obesity"],
    "ckd": ["age","bp","sg","al","su","rbc","pc","pcc","ba","bgr","bu","sc","sod","pot","hemo","pcv","wbcc",
            "rbcc","htn","dm","cad","appet","pe","ane"],
    "stroke": ["gender","age","hypertension","heart_disease","ever_married","work_type","Residence_type",
               "avg_glucose_level","bmi","smoking_status"],
}

STROKE_GROUPS = {
    "gender": ["gender_Female","gender_Male","gender_Other"],
    "ever_married": ["ever_married_No","ever_married_Yes"],
    "work_type": ["work_type_Govt_job","work_type_Never_worked","work_type_Private",
                   "work_type_Self-employed","work_type_children"],
    "Residence_type": ["Residence_type_Rural","Residence_type_Urban"],
    "smoking_status": ["smoking_status_Unknown","smoking_status_formerly smoked",
                       "smoking_status_never smoked","smoking_status_smokes"],
}

STROKE_DECODE = {
    "gender": {"gender_Female":"Female","gender_Male":"Male","gender_Other":"Other"},
    "ever_married": {"ever_married_No":"No","ever_married_Yes":"Yes"},
    "work_type": {
        "work_type_Govt_job":"Govt_job","work_type_Never_worked":"Never_worked",
        "work_type_Private":"Private","work_type_Self-employed":"Self-employed",
        "work_type_children":"children",
    },
    "Residence_type": {"Residence_type_Rural":"Rural","Residence_type_Urban":"Urban"},
    "smoking_status": {
        "smoking_status_Unknown":"Unknown","smoking_status_formerly smoked":"formerly smoked",
        "smoking_status_never smoked":"never smoked","smoking_status_smokes":"smokes",
    },
}


def decode_stroke_row(row: pd.Series) -> dict[str, Any]:
    out: dict[str, Any] = {}
    numeric = ["age","hypertension","heart_disease","avg_glucose_level","bmi"]
    for f in numeric:
        out[f] = row.get(f, np.nan)

    for raw_name, cols in STROKE_GROUPS.items():
        active = None
        for c in cols:
            if c in row.index:
                try:
                    if float(row[c]) == 1.0:
                        active = STROKE_DECODE[raw_name][c]
                        break
                except Exception:
                    pass
        if active is None:
            active = "Unknown" if raw_name == "smoking_status" else list(STROKE_DECODE[raw_name].values())[0]
        out[raw_name] = active

    if "stroke" in row.index:
        out["stroke"] = row["stroke"]
    elif "target" in row.index:
        out["target"] = row["target"]
    elif "Outcome" in row.index:
        out["Outcome"] = row["Outcome"]
    return out


def load_test_data(disease: str) -> pd.DataFrame:
    path = TEST_FILES[disease]
    if not path.exists():
        raise FileNotFoundError(f"Missing test dataset: {path}")
    df = pd.read_csv(path)
    if disease == "stroke":
        df = pd.DataFrame([decode_stroke_row(r) for _, r in df.iterrows()])
    return df


def target_column(df: pd.DataFrame) -> str | None:
    for c in ["target","Outcome","stroke","CKD","classification","class","label"]:
        if c in df.columns:
            return c
    return None


def clean_value(x: Any) -> Any:
    if isinstance(x, np.generic):
        return x.item()
    if pd.isna(x) if not isinstance(x, (list, tuple, dict)) else False:
        return None
    return x


def as_feature_vector(row: pd.Series, disease: str) -> Any:
    features = RAW_FEATURES[disease]
    vals = [clean_value(row.get(f)) for f in features]
    if disease == "stroke":
        return {f: vals[i] for i, f in enumerate(features)}
    return vals


def normalize_explanation(items: Any) -> list[dict[str, float]]:
    result: list[dict[str, float]] = []
    if not isinstance(items, list):
        return result
    for item in items:
        if not isinstance(item, dict):
            continue
        name = item.get("feature")
        impact = item.get("impact")
        if name is None or impact is None:
            continue
        try:
            result.append({"feature": str(name), "impact": float(impact)})
        except Exception:
            continue
    return result


def agreement(shap_items: list[dict[str, float]], lime_items: list[dict[str, float]]) -> dict[str, Any]:
    raw = calculate_shap_lime_agreement(shap_items, lime_items, top_k=TOP_K)
    return raw if isinstance(raw, dict) else {}


def top_features(items: list[dict[str, float]]) -> set[str]:
    return {x["feature"] for x in items[:TOP_K]}


def cf_changed_features(cf: dict[str, Any]) -> set[str]:
    changes = cf.get("changes", {})
    if not isinstance(changes, dict):
        return set()
    return {str(k) for k in changes.keys()}


def canonical_alignment_feature(feature: Any, disease: str) -> str:
    """
    Convert SHAP/LIME display names or LIME threshold expressions
    into the raw feature names used by the counterfactual engine.

    This is used ONLY for explanation-counterfactual alignment.
    It does not modify the SHAP/LIME agreement calculation.
    """
    if feature is None:
        return ""

    text = str(feature).strip()
    normalized = text.lower().strip()

    # Remove common LIME threshold expressions.
    import re

    match = re.match(
        r"^([A-Za-z_][A-Za-z0-9_]*)\s*(?:<=|>=|<|>|=)",
        text
    )

    if match:
        normalized = match.group(1).lower().strip()

    # Remove common one-hot/value expression suffixes.
    normalized = normalized.replace(" = 0", "").replace(" = 1", "")

    aliases = {

        # --------------------------------------------------------
        # HEART
        # --------------------------------------------------------
        "heart": {
            "age": "age",
            "sex": "sex",
            "gender": "sex",

            "cp": "cp",
            "chest pain": "cp",
            "chest pain type": "cp",

            "trestbps": "trestbps",
            "resting blood pressure": "trestbps",
            "blood pressure": "trestbps",

            "chol": "chol",
            "cholesterol": "chol",
            "serum cholesterol": "chol",

            "fbs": "fbs",
            "fasting blood sugar": "fbs",

            "restecg": "restecg",
            "resting ecg": "restecg",

            "thalach": "thalach",
            "maximum heart rate": "thalach",
            "max heart rate": "thalach",

            "exang": "exang",
            "exercise angina": "exang",
            "exercise induced angina": "exang",

            "oldpeak": "oldpeak",
            "st depression": "oldpeak",

            "slope": "slope",
            "st slope": "slope",
            "slope of st segment": "slope",

            "ca": "ca",
            "major vessels": "ca",

            "thal": "thal",
            "thalassemia": "thal",
        },

        # --------------------------------------------------------
        # DIABETES
        # --------------------------------------------------------
        "diabetes": {
            "age": "age",
            "gender": "gender",
            "polyuria": "polyuria",
            "polydipsia": "polydipsia",
            "sudden weight loss": "sudden_weight_loss",
            "sudden_weight_loss": "sudden_weight_loss",
            "weakness": "weakness",
            "polyphagia": "polyphagia",
            "genital thrush": "genital_thrush",
            "genital_thrush": "genital_thrush",
            "visual blurring": "visual_blurring",
            "visual_blurring": "visual_blurring",
            "itching": "itching",
            "irritability": "irritability",
            "delayed healing": "delayed_healing",
            "delayed_healing": "delayed_healing",
            "partial paresis": "partial_paresis",
            "partial_paresis": "partial_paresis",
            "muscle stiffness": "muscle_stiffness",
            "muscle_stiffness": "muscle_stiffness",
            "alopecia": "alopecia",
            "obesity": "obesity",
        },

        # --------------------------------------------------------
        # CKD
        # --------------------------------------------------------
        "ckd": {
            "age": "age",
            "bp": "bp",
            "blood pressure": "bp",
            "sg": "sg",
            "specific gravity": "sg",
            "al": "al",
            "albumin": "al",
            "su": "su",
            "sugar": "su",
            "rbc": "rbc",
            "red blood cells": "rbc",
            "pc": "pc",
            "pus cell": "pc",
            "pcc": "pcc",
            "pus cell clumps": "pcc",
            "ba": "ba",
            "bacteria": "ba",
            "bgr": "bgr",
            "blood glucose random": "bgr",
            "bu": "bu",
            "blood urea": "bu",
            "sc": "sc",
            "serum creatinine": "sc",
            "sod": "sod",
            "sodium": "sod",
            "pot": "pot",
            "potassium": "pot",
            "hemo": "hemo",
            "hemoglobin": "hemo",
            "pcv": "pcv",
            "packed cell volume": "pcv",
            "wbcc": "wbcc",
            "white blood cell count": "wbcc",
            "rbcc": "rbcc",
            "red blood cell count": "rbcc",
            "htn": "htn",
            "hypertension": "htn",
            "dm": "dm",
            "diabetes mellitus": "dm",
            "cad": "cad",
            "coronary artery disease": "cad",
            "appet": "appet",
            "appetite": "appet",
            "pe": "pe",
            "pedal edema": "pe",
            "ane": "ane",
            "anemia": "ane",
        },

        # --------------------------------------------------------
        # STROKE
        # --------------------------------------------------------
        "stroke": {
            "age": "age",
            "hypertension": "hypertension",
            "heart disease": "heart_disease",
            "heart_disease": "heart_disease",
            "average glucose level": "avg_glucose_level",
            "avg_glucose_level": "avg_glucose_level",
            "blood glucose": "avg_glucose_level",
            "body mass index": "bmi",
            "bmi": "bmi",

            # One-hot encoded stroke features
            "gender_female": "gender",
            "gender_male": "gender",
            "gender_other": "gender",

            "marital status - no": "ever_married",
            "marital status - yes": "ever_married",
            "ever_married_no": "ever_married",
            "ever_married_yes": "ever_married",

            "work type - government job": "work_type",
            "work type - never worked": "work_type",
            "work type - private": "work_type",
            "work type - self-employed": "work_type",
            "work type - children": "work_type",

            "work_type_govt_job": "work_type",
            "work_type_never_worked": "work_type",
            "work_type_private": "work_type",
            "work_type_self-employed": "work_type",
            "work_type_children": "work_type",

            "residence type - rural": "Residence_type",
            "residence type - urban": "Residence_type",
            "residence_type_rural": "Residence_type",
            "residence_type_urban": "Residence_type",

            "smoking status - unknown": "smoking_status",
            "smoking status - formerly smoked": "smoking_status",
            "smoking status - never smoked": "smoking_status",
            "smoking status - smokes": "smoking_status",

            "smoking_status_unknown": "smoking_status",
            "smoking_status_formerly smoked": "smoking_status",
            "smoking_status_never smoked": "smoking_status",
            "smoking_status_smokes": "smoking_status",
        },
    }

    disease_aliases = aliases.get(
        str(disease).lower(),
        {}
    )

    return disease_aliases.get(
        normalized,
        normalized
    )


def alignment(
    cf_list: list[dict[str, Any]],
    shap_items: list[dict[str, float]],
    lime_items: list[dict[str, float]],
    disease: str = ""
) -> dict[str, Any]:

    shap_top = {
        canonical_alignment_feature(
            x["feature"],
            disease
        )
        for x in shap_items[:TOP_K]
    }

    lime_top = {
        canonical_alignment_feature(
            x["feature"],
            disease
        )
        for x in lime_items[:TOP_K]
    }

    common_top = shap_top & lime_top

    changed_sets = [
        cf_changed_features(cf)
        for cf in cf_list
    ]

    changed = set().union(
        *changed_sets
    ) if changed_sets else set()

    if not changed:
        return {
            "cf_count": 0,
            "cf_feature_count": 0,
            "shap_alignment_pct": np.nan,
            "lime_alignment_pct": np.nan,
            "common_alignment_pct": np.nan,
        }

    return {
        "cf_count": len(cf_list),
        "cf_feature_count": len(changed),

        "shap_alignment_pct":
            100.0 * len(
                changed & shap_top
            ) / len(changed),

        "lime_alignment_pct":
            100.0 * len(
                changed & lime_top
            ) / len(changed),

        "common_alignment_pct":
            100.0 * len(
                changed & common_top
            ) / len(changed),
    }
def evaluate_patient(row: pd.Series, disease: str) -> dict[str, Any]:
    features = as_feature_vector(row, disease)

    record: dict[str, Any] = {
        "disease": disease,
        "shap_ok": False,
        "lime_ok": False,
        "agreement_ok": False,
        "cf_ok": False,
        "cf_success": False,
    }

    try:
        shap_items = normalize_explanation(explain(features, disease=disease))
        record["shap_ok"] = bool(shap_items)
    except Exception as exc:
        record["shap_error"] = repr(exc)
        shap_items = []

    try:
        lime_items = normalize_explanation(lime_explain(features, disease=disease))
        record["lime_ok"] = bool(lime_items)
    except Exception as exc:
        record["lime_error"] = repr(exc)
        lime_items = []

    if shap_items and lime_items:
        try:
            ag = agreement(shap_items, lime_items)
            record.update({
                "feature_agreement": ag.get("feature_agreement_percentage", ag.get("feature_agreement", np.nan)),
                "direction_agreement": ag.get("direction_agreement_percentage", ag.get("direction_agreement", np.nan)),
                "ranking_agreement": ag.get("ranking_agreement_percentage", ag.get("ranking_agreement", np.nan)),
                "overall_consistency": ag.get("overall_consistency_score", ag.get("overall_consistency", np.nan)),
            })
            record["agreement_ok"] = True
        except Exception as exc:
            record["agreement_error"] = repr(exc)

    try:
        _, _, cfs = find_counterfactuals(
            features,
            disease=disease,
            max_results=MAX_CF_RESULTS,
            max_features_changed=3,
        )
        cfs = cfs if isinstance(cfs, list) else []
        record["cf_ok"] = True
        record["cf_success"] = len(cfs) > 0
        record.update(alignment(cfs, shap_items, lime_items, disease))
        record["cf_raw"] = json.dumps(cfs, default=str)
    except Exception as exc:
        record["cf_error"] = repr(exc)
        record.update({
            "cf_count": 0,
            "cf_feature_count": 0,
            "shap_alignment_pct": np.nan,
            "lime_alignment_pct": np.nan,
            "common_alignment_pct": np.nan,
        })

    return record


def safe_mean(series: pd.Series) -> float:
    numeric = pd.to_numeric(series, errors="coerce").dropna()
    return float(numeric.mean()) if len(numeric) else float("nan")


def main() -> None:
    print("=" * 70)
    print("XAI-CDSS FULL RESEARCH EVALUATION")
    print("=" * 70)
    print(f"Stroke threshold: {stroke_threshold}")

    all_rows = []
    summary = []

    for disease in ["heart", "diabetes", "ckd", "stroke"]:
        print(f"\n{'-'*70}\n{disease.upper()}\n{'-'*70}")
        df = load_test_data(disease)
        n = min(PATIENTS_PER_DISEASE, len(df))
        sample = df.sample(n=n, random_state=RANDOM_SEED)

        disease_rows = []
        for idx, (_, row) in enumerate(sample.iterrows(), start=1):
            print(f"Patient {idx}/{n} ...", end=" ")
            r = evaluate_patient(row, disease)
            r["patient_index"] = idx
            disease_rows.append(r)
            print("OK")
        all_rows.extend(disease_rows)

        ddf = pd.DataFrame(disease_rows)
        summary.append({
            "disease": disease,
            "patients_evaluated": len(ddf),
            "agreement_valid_cases": int(ddf["agreement_ok"].sum()),
            "mean_feature_agreement_pct": safe_mean(ddf.get("feature_agreement", pd.Series(dtype=float))),
            "mean_direction_agreement_pct": safe_mean(ddf.get("direction_agreement", pd.Series(dtype=float))),
            "mean_ranking_agreement_pct": safe_mean(ddf.get("ranking_agreement", pd.Series(dtype=float))),
            "mean_overall_consistency_pct": safe_mean(ddf.get("overall_consistency", pd.Series(dtype=float))),
            "counterfactual_valid_cases": int(ddf["cf_ok"].sum()),
            "counterfactual_success_cases": int(ddf["cf_success"].sum()),
            "counterfactual_success_rate_pct": 100.0 * float(ddf["cf_success"].mean()) if len(ddf) else np.nan,
            "mean_cf_count": safe_mean(ddf.get("cf_count", pd.Series(dtype=float))),
            "mean_cf_feature_count": safe_mean(ddf.get("cf_feature_count", pd.Series(dtype=float))),
            "mean_shap_cf_alignment_pct": safe_mean(ddf.get("shap_alignment_pct", pd.Series(dtype=float))),
            "mean_lime_cf_alignment_pct": safe_mean(ddf.get("lime_alignment_pct", pd.Series(dtype=float))),
            "mean_common_cf_alignment_pct": safe_mean(ddf.get("common_alignment_pct", pd.Series(dtype=float))),
        })

    detailed = pd.DataFrame(all_rows)
    summary_df = pd.DataFrame(summary)

    detailed.to_csv(RESULTS_DIR / "full_research_detailed.csv", index=False)
    summary_df.to_csv(RESULTS_DIR / "full_research_summary.csv", index=False)

    # Baseline/ablation tables: no fabricated values.
    baseline = pd.DataFrame({
        "component": [
            "Prediction-only",
            "Prediction + SHAP",
            "Prediction + LIME",
            "Prediction + SHAP + LIME",
            "Prediction + SHAP + LIME + Agreement",
            "Full framework + Counterfactual Alignment",
        ],
        "classification_metric_source": [
            "Production model test evaluation",
            "Same production model; explanation added",
            "Same production model; explanation added",
            "Same production model; dual explanations",
            "Same production model; agreement metrics",
            "Same production model; CF alignment",
        ],
        "metric_value": [np.nan] * 6,
        "note": "Classification performance is unchanged by post-hoc explanation layers; populate model metrics from held-out test evaluation files."
    })
    baseline.to_csv(RESULTS_DIR / "baseline_comparison_template.csv", index=False)

    ablation = pd.DataFrame({
        "configuration": [
            "Prediction only",
            "Prediction + SHAP",
            "Prediction + LIME",
            "Prediction + SHAP + LIME",
            "Full XAI-CDSS",
        ],
        "feature_agreement_pct": [np.nan] * 5,
        "overall_consistency_pct": [np.nan] * 5,
        "cf_success_rate_pct": [np.nan] * 5,
        "alignment_pct": [np.nan] * 5,
        "interpretation": [
            "No explanation layer",
            "Single global/local attribution path",
            "Single local surrogate path",
            "Dual-explainer configuration",
            "Dual explainers + agreement + counterfactual validation",
        ],
    })
    ablation.to_csv(RESULTS_DIR / "ablation_template.csv", index=False)

    print("\n" + "=" * 70)
    print("COMPLETED")
    print("=" * 70)
    print(summary_df.to_string(index=False))
    print("\nSaved:")
    print(RESULTS_DIR / "full_research_detailed.csv")
    print(RESULTS_DIR / "full_research_summary.csv")
    print(RESULTS_DIR / "baseline_comparison_template.csv")
    print(RESULTS_DIR / "ablation_template.csv")


if __name__ == "__main__":
    main()
