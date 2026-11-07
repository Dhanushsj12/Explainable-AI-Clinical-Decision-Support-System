"""Cross-Explainer Concordance Index (CECI) for SHAP and LIME outputs."""

import re


# SHAP uses clinical display labels, whereas LIME uses model column names.
# Both must refer to the same canonical name before agreement is calculated.
FEATURE_ALIASES = {
    "age": "age", "gender": "sex", "sex": "sex",
    "chest pain type": "cp", "cp": "cp",
    "resting blood pressure": "trestbps", "trestbps": "trestbps",
    "cholesterol": "chol", "chol": "chol",
    "fasting blood sugar": "fbs", "fbs": "fbs",
    "resting ecg": "restecg", "restecg": "restecg",
    "maximum heart rate": "thalach", "thalach": "thalach",
    "exercise angina": "exang", "exercise induced angina": "exang", "exang": "exang",
    "st depression": "oldpeak", "oldpeak": "oldpeak",
    "slope of st segment": "slope", "slope": "slope",
    "major vessels": "ca", "ca": "ca", "thalassemia": "thal", "thal": "thal",
    "blood pressure": "bp", "bp": "bp", "specific gravity": "sg", "sg": "sg",
    "albumin": "al", "al": "al", "sugar": "su", "su": "su",
    "serum creatinine": "sc", "sc": "sc", "hemoglobin": "hemo", "hemo": "hemo",
    "average glucose level": "avg_glucose_level", "avg_glucose_level": "avg_glucose_level",
    "body mass index": "bmi", "bmi": "bmi", "hypertension": "hypertension",
    "heart disease status": "heart_disease", "heart_disease": "heart_disease",
    "smoking status": "smoking_status", "smoking_status": "smoking_status",
}


def _name(item):
    value = str(item.get("feature", "")).strip().lower()
    # LIME may produce either "cp <= 0.2" or "-0.99 < polyuria <= 1.01".
    # Remove a leading numeric interval before stripping the trailing threshold.
    value = re.sub(r"^[-+]?\d*\.?\d+\s*<\s*", "", value)
    value = re.split(r"\s*(?:<=|>=|<|>|=)\s*", value, maxsplit=1)[0]
    value = re.sub(r"\s+", " ", value).strip()
    return FEATURE_ALIASES.get(value, value)


def _impact(item):
    try:
        return float(item.get("impact", 0))
    except (TypeError, ValueError):
        return 0.0


def calculate_shap_lime_agreement(shap_features, lime_features, top_k=5):
    """Compute CECI = 0.40 overlap + 0.30 direction + 0.30 rank agreement."""
    shap = list(shap_features or [])[:top_k]
    lime = list(lime_features or [])[:top_k]
    shap_by_name = {_name(item): item for item in shap if _name(item)}
    lime_by_name = {_name(item): item for item in lime if _name(item)}

    shap_names = list(shap_by_name)
    lime_names = list(lime_by_name)
    common = [name for name in shap_names if name in lime_by_name]

    # The CECI paper defines overlap over the top-K evidence set, not Jaccard union.
    feature_agreement = 100 * len(common) / max(top_k, 1)
    direction_matches = sum(
        (_impact(shap_by_name[name]) >= 0) == (_impact(lime_by_name[name]) >= 0)
        for name in common
    )
    direction_agreement = 100 * direction_matches / len(common) if common else 0.0

    if len(common) <= 1:
        ranking_agreement = 100.0 if common else 0.0
    else:
        mean_rank_distance = sum(
            abs(shap_names.index(name) - lime_names.index(name))
            for name in common
        ) / len(common)
        ranking_agreement = max(0.0, 100 * (1 - mean_rank_distance / (top_k - 1)))
    score = round(
        0.40 * feature_agreement +
        0.30 * direction_agreement +
        0.30 * ranking_agreement,
        2
    )

    return {
        "feature_agreement_percentage": round(feature_agreement, 2),
        "direction_agreement_percentage": round(direction_agreement, 2),
        "ranking_agreement_percentage": round(ranking_agreement, 2),
        "overall_consistency_score": score,
        "consistency_level": "High" if score >= 80 else "Moderate" if score >= 50 else "Low",
        "common_features": common,
        "shap_only_features": [name for name in shap_names if name not in lime_by_name],
        "lime_only_features": [name for name in lime_names if name not in shap_by_name],
        "metric_name": "CECI",
    }
