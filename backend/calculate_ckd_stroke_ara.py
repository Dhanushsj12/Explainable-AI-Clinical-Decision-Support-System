import json
import random
from pathlib import Path

from prediction import predict, CKD_FEATURES, STROKE_FEATURES
from explainability import explain
from app import get_lime_explanation, calculate_counterfactuals
from attribution_recourse_alignment import calculate_ara, _name


CASES = {
    "CKD Low Risk": {
        "disease": "ckd",
        "features": {
            "age": 35,
            "bp": 70,
            "sg": 1.020,
            "al": 0,
            "su": 0,
            "rbc": 0,
            "pc": 0,
            "pcc": 0,
            "ba": 0,
            "bgr": 100,
            "bu": 20,
            "sc": 0.8,
            "sod": 140,
            "pot": 4.2,
            "hemo": 15,
            "pcv": 45,
            "wbcc": 7500,
            "rbcc": 5.0,
            "htn": 0,
            "dm": 0,
            "cad": 0,
            "appet": 1,
            "pe": 0,
            "ane": 0,
        },
    },
    "CKD High Risk": {
        "disease": "ckd",
        "features": {
            "age": 60,
            "bp": 100,
            "sg": 1.020,
            "al": 4,
            "su": 2,
            "rbc": 1,
            "pc": 1,
            "pcc": 1,
            "ba": 1,
            "bgr": 220,
            "bu": 80,
            "sc": 4.0,
            "sod": 130,
            "pot": 6.2,
            "hemo": 9,
            "pcv": 28,
            "wbcc": 12000,
            "rbcc": 3.2,
            "htn": 1,
            "dm": 1,
            "cad": 1,
            "appet": 0,
            "pe": 1,
            "ane": 1,
        },
    },
    "Stroke Low Risk": {
        "disease": "stroke",
        "features": {
            "gender": "Female",
            "age": 35,
            "hypertension": 0,
            "heart_disease": 0,
            "ever_married": "No",
            "work_type": "Private",
            "Residence_type": "Urban",
            "avg_glucose_level": 85,
            "bmi": 22,
            "smoking_status": "never smoked",
        },
    },
    "Stroke High Risk": {
        "disease": "stroke",
        "features": {
            "gender": "Female",
            "age": 79,
            "hypertension": 1,
            "heart_disease": 0,
            "ever_married": "Yes",
            "work_type": "Self-employed",
            "Residence_type": "Rural",
            "avg_glucose_level": 174.12,
            "bmi": 42,
            "smoking_status": "never smoked",
        },
    },
}


def random_baseline(recourse_features, available_features, trials=10000):
    """Expected ARA when five features are selected randomly."""
    recourse = set(recourse_features)

    if not recourse:
        return 0.0

    feature_pool = list(
        {_name(feature) for feature in available_features}
    )

    sample_size = min(5, len(feature_pool))
    rng = random.Random(42)
    scores = []

    for _ in range(trials):
        selected = set(
            rng.sample(feature_pool, sample_size)
        )

        score = (
            100
            * len(selected.intersection(recourse))
            / len(recourse)
        )

        scores.append(score)

    return round(sum(scores) / len(scores), 2)


def evaluate_case(case_name, disease, features):
    # CKD LIME requires a feature list in exact model-training order.
    # Stroke accepts the original feature dictionary.
    if disease == "ckd":
        model_features = [
            features[feature]
            for feature in CKD_FEATURES
        ]
    else:
        model_features = features

    prediction_result = predict(
        model_features,
        disease
    )

    prediction_class = int(
        prediction_result["prediction_class"]
    )

    probability = float(
        prediction_result["probability"]
    )

    shap_features = explain(
        model_features,
        disease
    ) or []

    lime_features = get_lime_explanation(
        model_features,
        disease
    ) or []

    counterfactual_result = calculate_counterfactuals(
        features=model_features,
        disease=disease,
        original_prediction=prediction_class,
        original_probability=probability,
        max_results=5,
    )

    scenarios = counterfactual_result.get(
        "counterfactuals",
        []
    )

    ara = calculate_ara(
        shap_features,
        lime_features,
        scenarios,
        top_k=5,
    )

    available_features = (
        CKD_FEATURES
        if disease == "ckd"
        else STROKE_FEATURES
    )

    baseline = random_baseline(
        ara["recourse_features"],
        available_features,
    )

    return {
        "case": case_name,
        "disease": disease,
        "prediction": prediction_result.get("prediction"),
        "prediction_class": prediction_class,
        "probability_percentage": probability,
        "shap_alignment_percentage": ara[
            "shap_alignment_percentage"
        ],
        "lime_alignment_percentage": ara[
            "lime_alignment_percentage"
        ],
        "mean_alignment_percentage": ara[
            "mean_alignment_percentage"
        ],
        "random_baseline_percentage": baseline,
        "recourse_features": ara["recourse_features"],
        "shap_shared_features": ara[
            "shap_shared_features"
        ],
        "lime_shared_features": ara[
            "lime_shared_features"
        ],
        "scenario_count": len(scenarios),
    }


def main():
    results = []

    for case_name, case_data in CASES.items():
        results.append(
            evaluate_case(
                case_name,
                case_data["disease"],
                case_data["features"],
            )
        )

    base_path = Path(__file__).resolve().parent

    json_path = (
        base_path / "ara_ckd_stroke_results.json"
    )

    summary_path = (
        base_path / "ara_ckd_stroke_summary.txt"
    )

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)

    lines = [
        "CKD and Stroke ARA Results",
        "=" * 60,
    ]

    for result in results:
        lines.extend([
            "",
            f"Case: {result['case']}",
            (
                f"Prediction: {result['prediction']} "
                f"({result['probability_percentage']}%)"
            ),
            (
                f"SHAP ARA: "
                f"{result['shap_alignment_percentage']}%"
            ),
            (
                f"LIME ARA: "
                f"{result['lime_alignment_percentage']}%"
            ),
            (
                f"Mean ARA: "
                f"{result['mean_alignment_percentage']}%"
            ),
            (
                f"Random baseline: "
                f"{result['random_baseline_percentage']}%"
            ),
            (
                "Recourse features: "
                + ", ".join(result["recourse_features"])
            ),
            (
                f"Scenarios evaluated: "
                f"{result['scenario_count']}"
            ),
        ])

    summary_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("Completed successfully.")
    print(f"Summary saved to: {summary_path}")
    print(f"JSON saved to: {json_path}")


if __name__ == "__main__":
    main()