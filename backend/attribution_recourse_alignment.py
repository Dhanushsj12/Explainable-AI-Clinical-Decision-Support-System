"""Attribution-to-Recourse Alignment (ARA) for the academic XAI-CDSS."""

import re


ALIASES = {
    "sex": "gender", "gender": "gender", "cp": "chest pain type",
    "trestbps": "resting blood pressure", "chol": "cholesterol",
    "fbs": "fasting blood sugar", "restecg": "resting ecg",
    "thalach": "maximum heart rate", "exang": "exercise angina",
    "oldpeak": "st depression", "slope": "slope of st segment",
    "ca": "major vessels", "thal": "thalassemia",
    "genital_thrush": "genital thrush", "muscle_stiffness": "muscle stiffness",
    "delayed_healing": "delayed healing", "partial_paresis": "partial paresis",
    "sudden_weight_loss": "sudden weight loss", "visual_blurring": "visual blurring",
    "blood pressure": "bp", "specific gravity": "sg", "albumin": "al",
    "sugar": "su", "blood glucose": "bgr", "blood urea": "bu",
    "serum creatinine": "sc", "sodium": "sod", "potassium": "pot",
    "hemoglobin": "hemo", "packed cell volume": "pcv",
    "white blood cell count": "wbcc", "red blood cell count": "rbcc",
    "diabetes mellitus": "dm", "coronary artery disease": "cad",
    "pedal edema": "pe", "anemia": "ane",
}


def _name(item):
    value = str(item.get("feature", item) if isinstance(item, dict) else item).strip().lower()
    value = re.sub(r"^[-+]?\d*\.?\d+\s*<\s*", "", value)
    value = re.split(r"\s*(?:<=|>=|<|>|=)\s*", value, maxsplit=1)[0]
    value = re.sub(r"[_\s]+", " ", value).strip()
    return ALIASES.get(value, value)


def calculate_ara(shap_features, lime_features, counterfactuals, top_k=5):
    """Measure top-K explainer overlap with features changed by recourse.

    ARA is an explanatory alignment measure only; it does not validate a
    treatment or establish clinical causality.
    """
    recourse = set()
    for item in counterfactuals or []:
        recourse.update(_name(feature) for feature in (item.get("changes") or {}))
    shap = [_name(item) for item in (shap_features or [])[:top_k]]
    lime = [_name(item) for item in (lime_features or [])[:top_k]]
    shap_shared = [name for name in shap if name in recourse]
    lime_shared = [name for name in lime if name in recourse]
    denominator = len(recourse)
    shap_score = 100 * len(set(shap_shared)) / denominator if denominator else 0.0
    lime_score = 100 * len(set(lime_shared)) / denominator if denominator else 0.0
    return {
        "shap_alignment_percentage": round(shap_score, 2),
        "lime_alignment_percentage": round(lime_score, 2),
        "mean_alignment_percentage": round((shap_score + lime_score) / 2, 2),
        "recourse_features": sorted(recourse),
        "shap_shared_features": sorted(set(shap_shared)),
        "lime_shared_features": sorted(set(lime_shared)),
        "note": "ARA measures overlap between model explanations and hypothetical recourse features; it is not clinical validation.",
    }
