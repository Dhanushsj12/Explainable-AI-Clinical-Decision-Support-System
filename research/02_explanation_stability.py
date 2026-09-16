"""
02_explanation_stability.py

Research-only experiment:
Measure explanation stability for SHAP and LIME
under small perturbations of real held-out patients.

DO NOT modify production files.
"""

from pathlib import Path
import sys
import warnings

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

warnings.filterwarnings("ignore")


# ============================================================
# PROJECT PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"

sys.path.insert(0, str(BACKEND))


# ============================================================
# EXISTING PRODUCTION XAI FUNCTIONS
# ============================================================

from explainability import explain
from lime_explain import lime_explain


# ============================================================
# DATASETS
# ============================================================

DATASETS = {
    "heart":
        ROOT / "datasets/augmented/heart/heart_test_real.csv",

    "diabetes":
        ROOT / "datasets/augmented/diabetes/diabetes_test_real.csv",

    "ckd":
        ROOT / "datasets/augmented/ckd/ckd_test_real.csv",

    "stroke":
        ROOT / "datasets/augmented/stroke/stroke_test_real.csv",
}


# ============================================================
# EXPERIMENT SETTINGS
# ============================================================

RANDOM_SEED = 42

# Start small because LIME is computationally expensive.
MAX_PATIENTS_PER_DISEASE = 10

# Five local perturbations per patient.
N_PERTURBATIONS = 5

# Existing application explanations use top 5.
TOP_K = 5

# Maximum relative numerical perturbation.
PERTURBATION_RATE = 0.05

# Maximum absolute numerical movement.
MAX_STEP = 10.0


# ============================================================
# FEATURE GROUPS
# ============================================================

CATEGORICAL_FEATURES = {
    "heart": {
        "sex",
        "cp",
        "fbs",
        "restecg",
        "exang",
        "slope",
        "ca",
        "thal",
    },

    "diabetes": {
        "gender",
        "polyuria",
        "polydipsia",
        "sudden_weight_loss",
        "weakness",
        "polyphagia",
        "genital_thrush",
        "visual_blurring",
        "itching",
        "irritability",
        "delayed_healing",
        "partial_paresis",
        "muscle_stiffness",
        "alopecia",
        "obesity",
    },

    "ckd": {
        "hypertension",
        "diabetes_mellitus",
        "coronary_artery_disease",
        "appetite",
        "pedal_edema",
        "anemia",
    },

    "stroke": {
        "gender",
        "hypertension",
        "heart_disease",
        "ever_married",
        "work_type",
        "residence_type",
        "smoking_status",
    },
}


# ============================================================
# TARGET COLUMN CANDIDATES
# ============================================================

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
# TARGET DETECTION
# ============================================================

def find_target_column(df):

    for column in TARGET_CANDIDATES:

        if column in df.columns:
            return column

    raise ValueError(
        "Target column could not be identified.\n"
        f"Columns found: {list(df.columns)}"
    )


# ============================================================
# SAFE NUMERIC
# ============================================================

def to_float(value):

    try:
        return float(value)

    except (
        TypeError,
        ValueError,
    ):
        return None


# ============================================================
# NORMALIZE FEATURE NAME
# ============================================================

def normalize_feature_name(name):

    text = str(name).strip().lower()

    return text


# ============================================================
# NORMALIZE EXPLANATION RESULT
# ============================================================

def normalize_explanation(result):

    if result is None:
        return []

    # Existing SHAP/LIME functions return list.
    if isinstance(result, dict):

        for key in [
            "shap_features",
            "shap_values",
            "lime_features",
            "features",
            "explanation",
        ]:

            if key in result:

                result = result[key]

                break

    if not isinstance(
        result,
        list,
    ):
        return []

    output = []

    for item in result:

        if not isinstance(
            item,
            dict,
        ):
            continue

        feature = (
            item.get("feature")
            or item.get("name")
            or item.get("label")
        )

        impact = (
            item.get("impact")
        )

        if impact is None:
            impact = item.get(
                "value"
            )

        if impact is None:
            impact = item.get(
                "shap_value"
            )

        if impact is None:
            impact = item.get(
                "lime_value"
            )

        number = to_float(
            impact
        )

        if feature is None or number is None:
            continue

        output.append(
            {
                "feature":
                    str(feature),

                "normalized_feature":
                    normalize_feature_name(
                        feature
                    ),

                "impact":
                    number,
            }
        )

    output.sort(
        key=lambda x:
            abs(x["impact"]),
        reverse=True,
    )

    return output


# ============================================================
# TOP-K FEATURES
# ============================================================

def get_top_features(
    explanation,
):

    normalized = normalize_explanation(
        explanation
    )

    return [
        item[
            "normalized_feature"
        ]
        for item in normalized[:TOP_K]
    ]


# ============================================================
# IMPACT MAP
# ============================================================

def get_impact_map(
    explanation,
):

    normalized = normalize_explanation(
        explanation
    )

    return {
        item[
            "normalized_feature"
        ]:
        item["impact"]

        for item in normalized
    }


# ============================================================
# TOP-K OVERLAP
# ============================================================

def calculate_overlap(
    original,
    perturbed,
):

    original_features = set(
        get_top_features(
            original
        )
    )

    perturbed_features = set(
        get_top_features(
            perturbed
        )
    )

    denominator = max(
        len(original_features),
        len(perturbed_features),
        1,
    )

    return (
        len(
            original_features.intersection(
                perturbed_features
            )
        )
        /
        denominator
        *
        100.0
    )


# ============================================================
# SPEARMAN RANK CORRELATION
# ============================================================

def calculate_spearman(
    original,
    perturbed,
):

    original_map = get_impact_map(
        original
    )

    perturbed_map = get_impact_map(
        perturbed
    )

    common = list(
        set(original_map).intersection(
            perturbed_map
        )
    )

    if len(common) < 2:
        return np.nan

    original_values = [
        abs(original_map[x])
        for x in common
    ]

    perturbed_values = [
        abs(perturbed_map[x])
        for x in common
    ]

    correlation, _ = spearmanr(
        original_values,
        perturbed_values,
    )

    return float(
        correlation
    )


# ============================================================
# SIGN CONSISTENCY
# ============================================================

def calculate_sign_consistency(
    original,
    perturbed,
):

    original_map = get_impact_map(
        original
    )

    perturbed_map = get_impact_map(
        perturbed
    )

    common = set(
        original_map
    ).intersection(
        perturbed_map
    )

    if not common:
        return np.nan

    comparisons = 0
    matches = 0

    for feature in common:

        a = original_map[
            feature
        ]

        b = perturbed_map[
            feature
        ]

        if a == 0 or b == 0:
            continue

        comparisons += 1

        if (
            np.sign(a)
            ==
            np.sign(b)
        ):

            matches += 1

    if comparisons == 0:
        return np.nan

    return (
        matches
        /
        comparisons
        *
        100.0
    )


# ============================================================
# ATTRIBUTION CHANGE
# ============================================================

def calculate_attribution_change(
    original,
    perturbed,
):

    original_map = get_impact_map(
        original
    )

    perturbed_map = get_impact_map(
        perturbed
    )

    features = (
        set(original_map)
        |
        set(perturbed_map)
    )

    if not features:
        return np.nan

    numerator = 0.0
    denominator = 0.0

    for feature in features:

        old = original_map.get(
            feature,
            0.0,
        )

        new = perturbed_map.get(
            feature,
            0.0,
        )

        numerator += abs(
            old - new
        )

        denominator += abs(
            old
        )

    if denominator == 0:
        return np.nan

    return (
        numerator
        /
        denominator
    )


# ============================================================
# STABILITY SCORE
# ============================================================

def attribution_stability_score(
    change,
):

    if not np.isfinite(
        change
    ):
        return np.nan

    return (
        1.0
        -
        min(
            float(change),
            1.0,
        )
    ) * 100.0


# ============================================================
# BUILD MODEL-READY FEATURE VECTOR
# ============================================================

def get_feature_vector(
    row,
    disease,
):

    disease = disease.lower()

    # ========================================================
    # STROKE
    # ========================================================
    # The Stroke dataset used for evaluation is one-hot encoded
    # into 21 model features.
    #
    # The production SHAP/LIME functions expect the original
    # 10 raw clinical features and perform the encoding
    # internally.
    # ========================================================

    if disease == "stroke":

        def find_existing(
            candidates
        ):
            for candidate in candidates:
                if candidate in row.index:
                    return candidate

            return None

        # ----------------------------------------------------
        # Gender
        # ----------------------------------------------------

        gender_columns = [
            "gender_Female",
            "gender_Male",
            "gender_Other",
        ]

        gender_column = find_existing(
            gender_columns
        )

        if gender_column is not None:

            gender = (
                gender_column
                .replace(
                    "gender_",
                    "",
                    1,
                )
            )

        else:

            gender = row.get(
                "gender"
            )

        # ----------------------------------------------------
        # Ever Married
        # ----------------------------------------------------

        married_columns = [
            "ever_married_No",
            "ever_married_Yes",
        ]

        married_column = find_existing(
            married_columns
        )

        if married_column is not None:

            ever_married = (
                married_column
                .replace(
                    "ever_married_",
                    "",
                    1,
                )
            )

        else:

            ever_married = row.get(
                "ever_married"
            )

        # ----------------------------------------------------
        # Work Type
        # ----------------------------------------------------

        work_columns = [
            "work_type_Govt_job",
            "work_type_Never_worked",
            "work_type_Private",
            "work_type_Self-employed",
            "work_type_children",
        ]

        work_column = find_existing(
            work_columns
        )

        if work_column is not None:

            work_type = (
                work_column
                .replace(
                    "work_type_",
                    "",
                    1,
                )
            )

        else:

            work_type = row.get(
                "work_type"
            )

        # ----------------------------------------------------
        # Residence Type
        # ----------------------------------------------------

        residence_columns = [
            "Residence_type_Rural",
            "Residence_type_Urban",
        ]

        residence_column = find_existing(
            residence_columns
        )

        if residence_column is not None:

            residence_type = (
                residence_column
                .replace(
                    "Residence_type_",
                    "",
                    1,
                )
            )

        else:

            residence_type = row.get(
                "Residence_type"
            )

        # ----------------------------------------------------
        # Smoking Status
        # ----------------------------------------------------

        smoking_columns = [
            "smoking_status_Unknown",
            "smoking_status_formerly smoked",
            "smoking_status_never smoked",
            "smoking_status_smokes",
        ]

        smoking_column = find_existing(
            smoking_columns
        )

        if smoking_column is not None:

            smoking_status = (
                smoking_column
                .replace(
                    "smoking_status_",
                    "",
                    1,
                )
            )

        else:

            smoking_status = row.get(
                "smoking_status"
            )

        # ----------------------------------------------------
        # Return exact production raw feature order.
        # ----------------------------------------------------

        return pd.Series(
            {
                "gender":
                    gender,

                "age":
                    row.get("age"),

                "hypertension":
                    row.get("hypertension"),

                "heart_disease":
                    row.get("heart_disease"),

                "ever_married":
                    ever_married,

                "work_type":
                    work_type,

                "Residence_type":
                    residence_type,

                "avg_glucose_level":
                    row.get(
                        "avg_glucose_level"
                    ),

                "bmi":
                    row.get("bmi"),

                "smoking_status":
                    smoking_status,
            }
        )

    # ========================================================
    # OTHER DISEASES
    # ========================================================

    target_column = find_target_column(
        row.to_frame().T
    )

    features = row.drop(
        labels=[
            target_column
        ]
    )

    features = features.drop(
        labels=[
            "data_source",
            "Unnamed: 0",
        ],
        errors="ignore",
    )

    return features

    disease = disease.lower()

    # --------------------------------------------------------
    # Stroke MUST receive the original 10 raw clinical
    # features. The production SHAP/LIME preprocessors perform
    # the one-hot encoding internally.
    # --------------------------------------------------------

    if disease == "stroke":

        stroke_features = [
            "gender",
            "age",
            "hypertension",
            "heart_disease",
            "ever_married",
            "work_type",
            "Residence_type",
            "avg_glucose_level",
            "bmi",
            "smoking_status",
        ]

        missing = [
            feature
            for feature in stroke_features
            if feature not in row.index
        ]

        if missing:

            raise ValueError(
                "Stroke dataset is missing required "
                f"raw features: {missing}"
            )

        return row[
            stroke_features
        ]

    # --------------------------------------------------------
    # All other diseases
    # --------------------------------------------------------

    target_column = find_target_column(
        row.to_frame().T
    )

    features = row.drop(
        labels=[
            target_column
        ]
    )

    features = features.drop(
        labels=[
            "data_source",
            "Unnamed: 0",
        ],
        errors="ignore",
    )

    return features

    disease = disease.lower()

    target = find_target_column(
        row.to_frame().T
    )

    features = row.drop(
        labels=[
            target
        ]
    )

    # Remove bookkeeping fields.
    features = features.drop(
        labels=[
            "data_source",
            "Unnamed: 0",
        ],
        errors="ignore",
    )

    return features


# ============================================================
# PERTURB PATIENT
# ============================================================

def perturb_patient(
    row,
    disease,
    dataset,
    rng,
):

    result = row.copy()

    possible_features = [
        col
        for col in dataset.columns
        if col != find_target_column(dataset)
        and col not in [
            "data_source",
            "Unnamed: 0",
        ]
    ]

    rng.shuffle(
        possible_features
    )

    categorical = CATEGORICAL_FEATURES.get(
        disease,
        set(),
    )

    for feature in possible_features:

        old_value = result[
            feature
        ]

        # ----------------------------------------------------
        # CATEGORICAL
        # ----------------------------------------------------

        if feature.lower() in categorical:

            values = (
                pd.Series(
                    dataset[feature]
                )
                .dropna()
                .unique()
                .tolist()
            )

            if len(values) < 2:
                continue

            alternatives = [
                value
                for value in values
                if str(value)
                != str(old_value)
            ]

            if not alternatives:
                continue

            new_value = rng.choice(
                alternatives
            )

        # ----------------------------------------------------
        # NUMERICAL
        # ----------------------------------------------------

        else:

            number = to_float(
                old_value
            )

            if number is None:
                continue

            step = max(
                abs(number)
                *
                PERTURBATION_RATE,
                1.0,
            )

            step = min(
                step,
                MAX_STEP,
            )

            delta = rng.uniform(
                -step,
                step,
            )

            new_value = (
                number
                +
                delta
            )

        # Make sure something really changed.
        if str(new_value) == str(old_value):
            continue

        result[
            feature
        ] = new_value

        return (
            result,
            feature,
        )

    return (
        result,
        None,
    )


# ============================================================
# SHAP
# ============================================================

def run_shap(
    row,
    disease,
):

    vector = get_feature_vector(
        row,
        disease,
    )

    result = explain(
        vector.tolist(),
        disease=disease,
    )

    normalized = normalize_explanation(
        result
    )

    if not normalized:

        raise RuntimeError(
            f"SHAP explanation returned no features "
            f"for {disease}."
        )

    return normalized


# ============================================================
# LIME
# ============================================================

def run_lime(
    row,
    disease,
):

    vector = get_feature_vector(
        row,
        disease,
    )

    result = lime_explain(
        vector.tolist(),
        disease=disease,
    )

    normalized = normalize_explanation(
        result
    )

    if not normalized:

        raise RuntimeError(
            f"LIME explanation returned no features "
            f"for {disease}."
        )

    return normalized


# ============================================================
# SINGLE PATIENT
# ============================================================

def evaluate_patient(
    row,
    disease,
    dataset,
    patient_number,
    rng,
):

    print()
    print(
        "-" * 70
    )

    print(
        f"{disease.upper()} | "
        f"Patient #{patient_number}"
    )

    try:

        original_shap = run_shap(
            row,
            disease,
        )

        original_lime = run_lime(
            row,
            disease,
        )

    except Exception as exc:

        print(
            "Original explanation failed:"
        )

        print(
            repr(exc)
        )

        return []

    results = []

    for perturbation in range(
        1,
        N_PERTURBATIONS + 1,
    ):

        (
            perturbed_row,
            changed_feature,
        ) = perturb_patient(
            row,
            disease,
            dataset,
            rng,
        )

        if changed_feature is None:

            continue

        try:

            perturbed_shap = run_shap(
                perturbed_row,
                disease,
            )

            perturbed_lime = run_lime(
                perturbed_row,
                disease,
            )

        except Exception as exc:

            print(
                f"Perturbation "
                f"{perturbation} failed: "
                f"{exc}"
            )

            continue

        shap_overlap = (
            calculate_overlap(
                original_shap,
                perturbed_shap,
            )
        )

        shap_rank = (
            calculate_spearman(
                original_shap,
                perturbed_shap,
            )
        )

        shap_sign = (
            calculate_sign_consistency(
                original_shap,
                perturbed_shap,
            )
        )

        shap_change = (
            calculate_attribution_change(
                original_shap,
                perturbed_shap,
            )
        )

        lime_overlap = (
            calculate_overlap(
                original_lime,
                perturbed_lime,
            )
        )

        lime_rank = (
            calculate_spearman(
                original_lime,
                perturbed_lime,
            )
        )

        lime_sign = (
            calculate_sign_consistency(
                original_lime,
                perturbed_lime,
            )
        )

        lime_change = (
            calculate_attribution_change(
                original_lime,
                perturbed_lime,
            )
        )

        results.append(
            {
                "Disease":
                    disease,

                "Patient":
                    patient_number,

                "Perturbation":
                    perturbation,

                "Changed_Feature":
                    changed_feature,

                "SHAP_Top5_Overlap_Percent":
                    shap_overlap,

                "SHAP_Spearman":
                    shap_rank,

                "SHAP_Sign_Consistency_Percent":
                    shap_sign,

                "SHAP_Attribution_Change":
                    shap_change,

                "SHAP_Stability_Score":
                    attribution_stability_score(
                        shap_change
                    ),

                "LIME_Top5_Overlap_Percent":
                    lime_overlap,

                "LIME_Spearman":
                    lime_rank,

                "LIME_Sign_Consistency_Percent":
                    lime_sign,

                "LIME_Attribution_Change":
                    lime_change,

                "LIME_Stability_Score":
                    attribution_stability_score(
                        lime_change
                    ),
            }
        )

        print(
            f"Perturbation {perturbation}: "
            f"{changed_feature}"
        )

        print(
            f"  SHAP overlap = "
            f"{shap_overlap:.2f}% | "
            f"Spearman = "
            f"{shap_rank:.3f}"
            if np.isfinite(shap_rank)
            else
            f"  SHAP overlap = "
            f"{shap_overlap:.2f}% | "
            f"Spearman = NA"
        )

        print(
            f"  LIME overlap = "
            f"{lime_overlap:.2f}% | "
            f"Spearman = "
            f"{lime_rank:.3f}"
            if np.isfinite(lime_rank)
            else
            f"  LIME overlap = "
            f"{lime_overlap:.2f}% | "
            f"Spearman = NA"
        )

    return results


# ============================================================
# DISEASE
# ============================================================

def evaluate_disease(
    disease,
):

    path = DATASETS[
        disease
    ]

    dataset = pd.read_csv(
        path
    )

    # ONLY REAL TEST PATIENTS.
    sample = dataset.sample(
        n=min(
            MAX_PATIENTS_PER_DISEASE,
            len(dataset),
        ),
        random_state=RANDOM_SEED,
    )

    rng = np.random.default_rng(
        RANDOM_SEED
    )

    results = []

    for patient_number, (_, row) in enumerate(
        sample.iterrows(),
        start=1,
    ):

        patient_results = evaluate_patient(
            row,
            disease,
            dataset,
            patient_number,
            rng,
        )

        results.extend(
            patient_results
        )

    return results


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print(
        "XAI-CDSS EXPLANATION STABILITY EXPERIMENT"
    )
    print("=" * 70)

    all_results = []

    for disease in [
        "heart",
        "diabetes",
        "ckd",
        "stroke",
    ]:

        try:

            all_results.extend(
                evaluate_disease(
                    disease
                )
            )

        except Exception as exc:

            print()
            print(
                f"{disease.upper()} FAILED:"
            )

            print(
                repr(exc)
            )

    if not all_results:

        raise RuntimeError(
            "No stability results were produced."
        )

    detailed = pd.DataFrame(
        all_results
    )

    results_dir = (
        ROOT
        / "research"
        / "results"
    )

    results_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    detailed_file = (
        results_dir
        /
        "explanation_stability_detailed.csv"
    )

    summary_file = (
        results_dir
        /
        "explanation_stability_summary.csv"
    )

    detailed.to_csv(
        detailed_file,
        index=False,
    )

    summary = (
        detailed
        .groupby("Disease")
        .agg(
            Patients=(
                "Patient",
                "nunique",
            ),

            Perturbations=(
                "Perturbation",
                "count",
            ),

            SHAP_Overlap=(
                "SHAP_Top5_Overlap_Percent",
                "mean",
            ),

            SHAP_Spearman=(
                "SHAP_Spearman",
                "mean",
            ),

            SHAP_Sign=(
                "SHAP_Sign_Consistency_Percent",
                "mean",
            ),

            SHAP_Stability=(
                "SHAP_Stability_Score",
                "mean",
            ),

            LIME_Overlap=(
                "LIME_Top5_Overlap_Percent",
                "mean",
            ),

            LIME_Spearman=(
                "LIME_Spearman",
                "mean",
            ),

            LIME_Sign=(
                "LIME_Sign_Consistency_Percent",
                "mean",
            ),

            LIME_Stability=(
                "LIME_Stability_Score",
                "mean",
            ),
        )
        .reset_index()
    )

    summary.to_csv(
        summary_file,
        index=False,
    )

    print()
    print("=" * 70)
    print(
        "FINAL STABILITY RESULTS"
    )
    print("=" * 70)

    print(
        summary.to_string(
            index=False
        )
    )

    print()
    print(
        "Detailed:"
    )
    print(
        detailed_file
    )

    print()
    print(
        "Summary:"
    )
    print(
        summary_file
    )


if __name__ == "__main__":
    main()