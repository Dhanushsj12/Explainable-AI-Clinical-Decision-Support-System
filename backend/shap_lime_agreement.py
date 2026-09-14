import re


# ============================================================
# SUPPORTED DISEASES
# ============================================================

SUPPORTED_DISEASES = {
    "heart",
    "diabetes",
    "ckd",
    "stroke"
}


# ============================================================
# DISEASE NORMALIZATION
# ============================================================

def normalize_disease(disease):
    """
    Normalize disease names used by the backend/frontend.

    Supported:
        heart
        diabetes
        ckd
        stroke
    """

    if disease is None:
        return "heart"

    value = str(disease).strip().lower()

    aliases = {
        "heart": "heart",
        "heart disease": "heart",
        "heart_disease": "heart",
        "cardiac": "heart",

        "diabetes": "diabetes",
        "diabetic": "diabetes",

        "ckd": "ckd",
        "chronic kidney disease": "ckd",
        "chronic_kidney_disease": "ckd",
        "kidney": "ckd",

        "stroke": "stroke",
        "cerebrovascular": "stroke"
    }

    return aliases.get(
        value,
        value
    )


# ============================================================
# FEATURE DISPLAY NAMES
#
# Internal feature name -> frontend/PDF display name
# ============================================================

FEATURE_DISPLAY_NAMES = {

    # --------------------------------------------------------
    # HEART DISEASE
    # --------------------------------------------------------

    "heart": {

        "age":
            "Age",

        "sex":
            "Gender",

        "gender":
            "Gender",

        "cp":
            "Chest Pain Type",

        "trestbps":
            "Resting Blood Pressure",

        "chol":
            "Serum Cholesterol",

        "fbs":
            "Fasting Blood Sugar",

        "restecg":
            "Resting ECG",

        "thalach":
            "Maximum Heart Rate",

        "exang":
            "Exercise Angina",

        "oldpeak":
            "ST Depression",

        "slope":
            "ST Segment Slope",

        "ca":
            "Major Vessels",

        "thal":
            "Thalassemia"
    },


    # --------------------------------------------------------
    # DIABETES
    # --------------------------------------------------------

    "diabetes": {

        "age":
            "Age",

        "gender":
            "Gender",

        "sex":
            "Gender",

        "polyuria":
            "Polyuria",

        "polydipsia":
            "Polydipsia",

        "sudden_weight_loss":
            "Sudden Weight Loss",

        "weakness":
            "Weakness",

        "polyphagia":
            "Polyphagia",

        "genital_thrush":
            "Genital Thrush",

        "visual_blurring":
            "Visual Blurring",

        "itching":
            "Itching",

        "irritability":
            "Irritability",

        "delayed_healing":
            "Delayed Healing",

        "partial_paresis":
            "Partial Paresis",

        "muscle_stiffness":
            "Muscle Stiffness",

        "alopecia":
            "Alopecia",

        "obesity":
            "Obesity"
    },


    # --------------------------------------------------------
    # CHRONIC KIDNEY DISEASE
    # --------------------------------------------------------

    "ckd": {

        "age":
            "Age",

        "bp":
            "Blood Pressure",

        "sg":
            "Specific Gravity",

        "al":
            "Albumin",

        "su":
            "Sugar",

        "rbc":
            "Red Blood Cells",

        "pc":
            "Pus Cell",

        "pcc":
            "Pus Cell Clumps",

        "ba":
            "Bacteria",

        "bgr":
            "Blood Glucose",

        "blood_glucose":
            "Blood Glucose",

        "bu":
            "Blood Urea",

        "sc":
            "Serum Creatinine",

        "sod":
            "Sodium",

        "pot":
            "Potassium",

        "hemo":
            "Hemoglobin",

        "pcv":
            "Packed Cell Volume",

        "wbcc":
            "White Blood Cell Count",

        "rbcc":
            "Red Blood Cell Count",

        "htn":
            "Hypertension",

        "dm":
            "Diabetes Mellitus",

        "cad":
            "Coronary Artery Disease",

        "appet":
            "Appetite",

        "pe":
            "Pedal Edema",

        "ane":
            "Anemia"
    },


    # --------------------------------------------------------
    # STROKE
    # --------------------------------------------------------

    "stroke": {

        "age":
            "Age",

        "gender":
            "Gender",

        "sex":
            "Gender",

        "hypertension":
            "Hypertension",

        "heart_disease":
            "Heart Disease",

        "ever_married":
            "Ever Married",

        "work_type":
            "Work Type",

        "residence_type":
            "Residence Type",

        "residence":
            "Residence Type",

        "avg_glucose_level":
            "Average Glucose Level",

        "bmi":
            "Body Mass Index",

        "smoking_status":
            "Smoking Status"
    }
}


# ============================================================
# GLOBAL ALIASES
#
# These handle differences between:
#
# SHAP names
# LIME names
# model names
# frontend names
# PDF names
# ============================================================

GLOBAL_ALIASES = {

    # --------------------------------------------------------
    # HEART
    # --------------------------------------------------------

    "age":
        "age",

    "sex":
        "sex",

    "gender":
        "gender",

    "cp":
        "cp",

    "chest pain":
        "cp",

    "chest pain type":
        "cp",

    "trestbps":
        "trestbps",

    "resting blood pressure":
        "trestbps",

    "blood pressure":
        "trestbps",

    "chol":
        "chol",

    "cholesterol":
        "chol",

    "serum cholesterol":
        "chol",

    "fbs":
        "fbs",

    "fasting blood sugar":
        "fbs",

    "restecg":
        "restecg",

    "rest ecg":
        "restecg",

    "resting ecg":
        "restecg",

    "thalach":
        "thalach",

    "maximum heart rate":
        "thalach",

    "max heart rate":
        "thalach",

    "exang":
        "exang",

    "exercise angina":
        "exang",

    "exercise induced angina":
        "exang",

    "oldpeak":
        "oldpeak",

    "st depression":
        "oldpeak",

    "st depression (oldpeak)":
        "oldpeak",

    "slope":
        "slope",

    "st slope":
        "slope",

    "st segment slope":
        "slope",

    "ca":
        "ca",

    "major vessels":
        "ca",

    "thal":
        "thal",

    "thalassemia":
        "thal",


    # --------------------------------------------------------
    # DIABETES
    # --------------------------------------------------------

    "polyuria":
        "polyuria",

    "polydipsia":
        "polydipsia",

    "sudden weight loss":
        "sudden_weight_loss",

    "sudden_weight_loss":
        "sudden_weight_loss",

    "weakness":
        "weakness",

    "polyphagia":
        "polyphagia",

    "genital thrush":
        "genital_thrush",

    "genital_thrush":
        "genital_thrush",

    "visual blurring":
        "visual_blurring",

    "visual_blurring":
        "visual_blurring",

    "itching":
        "itching",

    "irritability":
        "irritability",

    "delayed healing":
        "delayed_healing",

    "delayed_healing":
        "delayed_healing",

    "partial paresis":
        "partial_paresis",

    "partial_paresis":
        "partial_paresis",

    "muscle stiffness":
        "muscle_stiffness",

    "muscle_stiffness":
        "muscle_stiffness",

    "alopecia":
        "alopecia",

    "obesity":
        "obesity",


    # --------------------------------------------------------
    # CKD
    # --------------------------------------------------------

    "specific gravity":
        "sg",

    "specific_gravity":
        "sg",

    "albumin":
        "al",

    "sugar":
        "su",

    "red blood cells":
        "rbc",

    "red_blood_cells":
        "rbc",

    "pus cell":
        "pc",

    "pus_cell":
        "pc",

    "pus cell clumps":
        "pcc",

    "pus_cell_clumps":
        "pcc",

    "bacteria":
        "ba",

    "blood glucose":
        "bgr",

    "blood glucose random":
        "bgr",

    "blood_glucose":
        "bgr",

    "blood_glucose_random":
        "bgr",

    "blood glucose random":
        "bgr",

    "blood urea":
        "bu",

    "serum creatinine":
        "sc",

    "sodium":
        "sod",

    "potassium":
        "pot",

    "hemoglobin":
        "hemo",

    "packed cell volume":
        "pcv",

    "white blood cell count":
        "wbcc",

    "white blood cell":
        "wbcc",

    "red blood cell count":
        "rbcc",

    "red blood cell":
        "rbcc",

    "hypertension":
        "htn",

    "diabetes mellitus":
        "dm",

    "diabetes mellitus":
        "dm",

    "coronary artery disease":
        "cad",

    "appetite":
        "appet",

    "pedal edema":
        "pe",

    "anemia":
        "ane",


    # --------------------------------------------------------
    # STROKE
    # --------------------------------------------------------

    "heart disease":
        "heart_disease",

    "heart_disease":
        "heart_disease",

    "ever married":
        "ever_married",

    "ever_married":
        "ever_married",

    "work type":
        "work_type",

    "work_type":
        "work_type",

    "residence type":
        "residence_type",

    "residence_type":
        "residence_type",

    "residence":
        "residence_type",

    "average glucose level":
        "avg_glucose_level",

    "average_glucose_level":
        "avg_glucose_level",

    "avg glucose level":
        "avg_glucose_level",

    "avg_glucose_level":
        "avg_glucose_level",

    "body mass index":
        "bmi",

    "body_mass_index":
        "bmi",

    "bmi":
        "bmi",

    "smoking status":
        "smoking_status",

    "smoking_status":
        "smoking_status",

    "hypertension":
        "htn"
}


# ============================================================
# FEATURE NORMALIZATION
# ============================================================

def normalize_feature_name(
    feature,
    disease=None
):
    """
    Convert SHAP/LIME feature names to a common
    internal feature name.

    Works for all four diseases.

    Examples:

        cp <= -0.16
            -> cp

        Polyuria
            -> polyuria

        -0.94 < delayed healing <= 1.06
            -> delayed_healing

        Average Glucose Level
            -> avg_glucose_level
    """

    if feature is None:
        return ""

    text = str(
        feature
    ).strip()

    if not text:
        return ""

    # --------------------------------------------------------
    # Remove common LIME numerical conditions.
    #
    # Supports:
    #
    # cp <= 0.5
    # age > 50
    # -0.7 < bmi <= 1.2
    # polyuria = 1
    # --------------------------------------------------------

    # First try the feature at the beginning.
    match = re.match(
        r"^\s*"
        r"([A-Za-z_][A-Za-z0-9_]*)"
        r"\s*(?:<=|>=|<|>|=)",
        text
    )

    if match:

        text = match.group(
            1
        )

    else:

        # Handle expressions where a numeric lower
        # bound appears before the feature.

        match = re.search(
            r"(?:<=|>=|<|>)\s*"
            r"([A-Za-z_][A-Za-z0-9_]*)",
            text
        )

        if match:

            text = match.group(
                1
            )

    # --------------------------------------------------------
    # Basic normalization
    # --------------------------------------------------------

    normalized = (
        text
        .strip()
        .lower()
    )

    normalized = normalized.replace(
        "-",
        "_"
    )

    normalized = re.sub(
        r"\s+",
        " ",
        normalized
    )

    # --------------------------------------------------------
    # Remove accidental trailing punctuation.
    # --------------------------------------------------------

    normalized = normalized.strip(
        " ,:;()[]{}"
    )

    # --------------------------------------------------------
    # Disease-specific map has priority.
    # --------------------------------------------------------

    disease_key = normalize_disease(
        disease
    )

    disease_map = FEATURE_DISPLAY_NAMES.get(
        disease_key,
        {}
    )

    if normalized in disease_map:
        return normalized

    # --------------------------------------------------------
    # Global aliases.
    # --------------------------------------------------------

    if normalized in GLOBAL_ALIASES:

        return GLOBAL_ALIASES[
            normalized
        ]

    # --------------------------------------------------------
    # Try underscore -> space.
    # --------------------------------------------------------

    spaced = normalized.replace(
        "_",
        " "
    )

    if spaced in GLOBAL_ALIASES:

        return GLOBAL_ALIASES[
            spaced
        ]

    # --------------------------------------------------------
    # Try compact comparison strings.
    # --------------------------------------------------------

    compact = re.sub(
        r"\s+",
        " ",
        normalized
    )

    if compact in GLOBAL_ALIASES:

        return GLOBAL_ALIASES[
            compact
        ]

    return normalized


# ============================================================
# DISPLAY NAME
# ============================================================

def display_feature_name(
    feature,
    disease=None
):
    """
    Return a human-readable feature label.
    """

    normalized = normalize_feature_name(
        feature,
        disease
    )

    disease_key = normalize_disease(
        disease
    )

    disease_map = FEATURE_DISPLAY_NAMES.get(
        disease_key,
        {}
    )

    if normalized in disease_map:

        return disease_map[
            normalized
        ]

    return (
        normalized
        .replace(
            "_",
            " "
        )
        .title()
    )


# ============================================================
# CONTRIBUTION DIRECTION
# ============================================================

def get_direction(
    impact
):
    """
    Determine explanation contribution direction.

    Positive:
        pushes toward positive/disease class.

    Negative:
        pushes away from positive/disease class.

    Neutral:
        zero or invalid contribution.
    """

    try:

        value = float(
            impact
        )

    except (
        TypeError,
        ValueError
    ):

        return "neutral"

    if value > 0:
        return "positive"

    if value < 0:
        return "negative"

    return "neutral"


# ============================================================
# EXPLANATION IMPACT
# ============================================================

def get_impact(
    item
):
    """
    Extract the numeric contribution from either
    SHAP or LIME result dictionaries.
    """

    if not isinstance(
        item,
        dict
    ):
        return 0.0

    for key in [

        "impact",

        "weight",

        "value",

        "contribution",

        "shap_value",

        "lime_value",

        "score"

    ]:

        if key in item:

            try:

                return float(
                    item[key]
                )

            except (
                TypeError,
                ValueError
            ):

                return 0.0

    return 0.0


# ============================================================
# NORMALIZE EXPLANATION LIST
# ============================================================

def normalize_explanation_list(
    results,
    disease=None
):
    """
    Normalize SHAP/LIME explanation dictionaries
    into one common representation.
    """

    if not isinstance(
        results,
        list
    ):
        return []

    normalized = []

    for item in results:

        if not isinstance(
            item,
            dict
        ):
            continue

        raw_feature = (
            item.get(
                "feature"
            )
            or
            item.get(
                "name"
            )
            or
            item.get(
                "label"
            )
            or
            ""
        )

        feature = normalize_feature_name(
            raw_feature,
            disease
        )

        if not feature:
            continue

        impact = get_impact(
            item
        )

        normalized.append({

            "feature":
                feature,

            "display_name":
                display_feature_name(
                    feature,
                    disease
                ),

            "impact":
                impact,

            "direction":
                get_direction(
                    impact
                )
        })

    return normalized


# ============================================================
# UNIQUE FEATURE ORDER
# ============================================================

def unique_features(
    results,
    disease=None
):
    """
    Return unique normalized feature names while
    preserving explanation order.
    """

    output = []

    for item in normalize_explanation_list(
        results,
        disease
    ):

        feature = item[
            "feature"
        ]

        if feature not in output:

            output.append(
                feature
            )

    return output


# ============================================================
# RANKING AGREEMENT
# ============================================================

def calculate_ranking_agreement(
    shap_features,
    lime_features
):
    """
    Calculate ranking similarity for features that
    occur in both SHAP and LIME.

    Score:
        100 = identical ranking
        0   = maximum disagreement

    Only common features are considered.
    """

    if not shap_features or not lime_features:

        return 0.0

    common = [

        feature

        for feature in shap_features

        if feature in lime_features

    ]

    # With zero or one common feature there is no
    # meaningful ranking disagreement.
    if len(common) <= 1:

        return 100.0

    shap_ranks = {

        feature:
            index + 1

        for index, feature
        in enumerate(
            shap_features
        )

        if feature in common
    }

    lime_ranks = {

        feature:
            index + 1

        for index, feature
        in enumerate(
            lime_features
        )

        if feature in common
    }

    rank_differences = []

    for feature in common:

        difference = abs(

            shap_ranks[
                feature
            ]

            -

            lime_ranks[
                feature
            ]

        )

        rank_differences.append(
            difference
        )

    if not rank_differences:

        return 100.0

    average_difference = (

        sum(
            rank_differences
        )

        /

        len(
            rank_differences
        )
    )

    max_possible_difference = (

        max(
            len(shap_features),
            len(lime_features)
        )

        -

        1
    )

    if max_possible_difference <= 0:

        return 100.0

    ranking_score = (

        1

        -

        (
            average_difference
            /
            max_possible_difference
        )

    ) * 100

    ranking_score = max(
        0.0,
        min(
            100.0,
            ranking_score
        )
    )

    return round(
        ranking_score,
        2
    )


# ============================================================
# DIRECTION AGREEMENT
# ============================================================

def calculate_direction_agreement(
    shap_results,
    lime_results,
    disease=None
):
    """
    Compare SHAP and LIME contribution directions
    for features identified by both methods.
    """

    shap_normalized = normalize_explanation_list(
        shap_results,
        disease
    )

    lime_normalized = normalize_explanation_list(
        lime_results,
        disease
    )

    shap_direction = {}

    for item in shap_normalized:

        shap_direction[
            item["feature"]
        ] = item["direction"]

    lime_direction = {}

    for item in lime_normalized:

        lime_direction[
            item["feature"]
        ] = item["direction"]

    common = [

        feature

        for feature in shap_direction

        if feature in lime_direction

    ]

    if not common:

        return {

            "direction_agreement_percentage":
                0.0,

            "direction_agreement":
                0.0,

            "direction_agreement_count":
                0,

            "direction_comparison_count":
                0,

            "direction_details":
                []
        }

    agreement_count = 0

    details = []

    for feature in common:

        shap_direction_value = (
            shap_direction[
                feature
            ]
        )

        lime_direction_value = (
            lime_direction[
                feature
            ]
        )

        agrees = (
            shap_direction_value
            ==
            lime_direction_value
        )

        if agrees:

            agreement_count += 1

        details.append({

            "feature":
                display_feature_name(
                    feature,
                    disease
                ),

            "shap_direction":
                shap_direction_value,

            "lime_direction":
                lime_direction_value,

            "agreement":
                agrees
        })

    percentage = (

        agreement_count
        /
        len(common)
        *
        100
    )

    percentage = round(
        percentage,
        2
    )

    return {

        "direction_agreement_percentage":
            percentage,

        "direction_agreement":
            percentage,

        "direction_agreement_count":
            agreement_count,

        "direction_comparison_count":
            len(common),

        "direction_details":
            details
    }


# ============================================================
# MAIN SHAP-LIME AGREEMENT
# ============================================================

def calculate_shap_lime_agreement(
    shap_results,
    lime_results,
    top_k=5,
    disease=None
):
    """
    Calculate SHAP/LIME explanation consistency for:

        Heart Disease
        Diabetes
        Chronic Kidney Disease
        Stroke

    Metrics:

        Feature Agreement   = 40%
        Direction Agreement = 30%
        Ranking Agreement   = 30%
    """

    if not isinstance(
        shap_results,
        list
    ):

        raise ValueError(
            "SHAP results must be a list."
        )

    if not isinstance(
        lime_results,
        list
    ):

        raise ValueError(
            "LIME results must be a list."
        )

    try:

        top_k = int(
            top_k
        )

    except (
        TypeError,
        ValueError
    ):

        top_k = 5

    if top_k <= 0:

        top_k = 5

    disease_key = normalize_disease(
        disease
    )

    # --------------------------------------------------------
    # Normalize complete explanation lists
    # --------------------------------------------------------

    shap_normalized = normalize_explanation_list(
        shap_results,
        disease_key
    )

    lime_normalized = normalize_explanation_list(
        lime_results,
        disease_key
    )

    # --------------------------------------------------------
    # Top K
    # --------------------------------------------------------

    shap_top = shap_normalized[
        :top_k
    ]

    lime_top = lime_normalized[
        :top_k
    ]

    # --------------------------------------------------------
    # Feature names
    # --------------------------------------------------------

    shap_features = [

        item[
            "feature"
        ]

        for item
        in shap_top

    ]

    lime_features = [

        item[
            "feature"
        ]

        for item
        in lime_top

    ]

    # --------------------------------------------------------
    # Remove duplicates while preserving order
    # --------------------------------------------------------

    shap_features = list(
        dict.fromkeys(
            shap_features
        )
    )

    lime_features = list(
        dict.fromkeys(
            lime_features
        )
    )

    # --------------------------------------------------------
    # Sets
    # --------------------------------------------------------

    shap_set = set(
        shap_features
    )

    lime_set = set(
        lime_features
    )

    # --------------------------------------------------------
    # Common features
    # --------------------------------------------------------

    common_features = [

        feature

        for feature
        in shap_features

        if feature in lime_set

    ]

    # --------------------------------------------------------
    # SHAP-only features
    # --------------------------------------------------------

    shap_only_features = [

        feature

        for feature
        in shap_features

        if feature not in lime_set

    ]

    # --------------------------------------------------------
    # LIME-only features
    # --------------------------------------------------------

    lime_only_features = [

        feature

        for feature
        in lime_features

        if feature not in shap_set

    ]

    # --------------------------------------------------------
    # Feature Agreement
    # --------------------------------------------------------

    denominator = max(

        len(shap_set),

        len(lime_set),

        1

    )

    overlap_count = len(
        common_features
    )

    feature_agreement = (

        overlap_count
        /
        denominator
        *
        100

    )

    feature_agreement = round(
        feature_agreement,
        2
    )

    # --------------------------------------------------------
    # Direction Agreement
    # --------------------------------------------------------

    direction_result = (
        calculate_direction_agreement(
            shap_top,
            lime_top,
            disease_key
        )
    )

    direction_agreement = (
        direction_result[
            "direction_agreement_percentage"
        ]
    )

    # --------------------------------------------------------
    # Ranking Agreement
    # --------------------------------------------------------

    ranking_agreement = (
        calculate_ranking_agreement(
            shap_features,
            lime_features
        )
    )

    # --------------------------------------------------------
    # Overall Consistency
    #
    # Feature Agreement   = 40%
    # Direction Agreement = 30%
    # Ranking Agreement   = 30%
    # --------------------------------------------------------

    overall_score = (

        feature_agreement
        * 0.40

        +

        direction_agreement
        * 0.30

        +

        ranking_agreement
        * 0.30

    )

    overall_score = round(
        overall_score,
        2
    )

    # --------------------------------------------------------
    # Consistency Level
    # --------------------------------------------------------

    if overall_score >= 80:

        consistency_level = "High"

    elif overall_score >= 50:

        consistency_level = "Moderate"

    else:

        consistency_level = "Low"

    # --------------------------------------------------------
    # Ordered feature groups
    # --------------------------------------------------------

    common_ordered = [

        feature

        for feature
        in shap_features

        if feature in common_features

    ]

    shap_only_ordered = [

        feature

        for feature
        in shap_features

        if feature in shap_only_features

    ]

    lime_only_ordered = [

        feature

        for feature
        in lime_features

        if feature in lime_only_features

    ]

    # --------------------------------------------------------
    # Human-readable feature names
    # --------------------------------------------------------

    common_display = [

        display_feature_name(
            feature,
            disease_key
        )

        for feature
        in common_ordered

    ]

    shap_only_display = [

        display_feature_name(
            feature,
            disease_key
        )

        for feature
        in shap_only_ordered

    ]

    lime_only_display = [

        display_feature_name(
            feature,
            disease_key
        )

        for feature
        in lime_only_ordered

    ]

    shap_display = [

        display_feature_name(
            feature,
            disease_key
        )

        for feature
        in shap_features

    ]

    lime_display = [

        display_feature_name(
            feature,
            disease_key
        )

        for feature
        in lime_features

    ]

    # --------------------------------------------------------
    # Final result
    #
    # Include BOTH long names and short aliases.
    # This keeps the backend, frontend and PDF compatible.
    # --------------------------------------------------------

    return {

        # ------------------------------------
        # Disease
        # ------------------------------------

        "disease":
            disease_key,

        "top_k":
            top_k,

        # ------------------------------------
        # Feature agreement
        # ------------------------------------

        "overlap_count":
            overlap_count,

        "shap_top_k_count":
            len(shap_features),

        "lime_top_k_count":
            len(lime_features),

        "feature_agreement":
            feature_agreement,

        "feature_agreement_percentage":
            feature_agreement,

        "overlap_percentage":
            feature_agreement,

        "overlap":
            feature_agreement,

        # ------------------------------------
        # Direction agreement
        # ------------------------------------

        "direction_agreement":
            direction_agreement,

        "direction_agreement_percentage":
            direction_agreement,

        "direction_agreement_count":
            direction_result[
                "direction_agreement_count"
            ],

        "direction_comparison_count":
            direction_result[
                "direction_comparison_count"
            ],

        "direction_details":
            direction_result[
                "direction_details"
            ],

        # ------------------------------------
        # Ranking agreement
        # ------------------------------------

        "ranking_agreement":
            ranking_agreement,

        "ranking_agreement_percentage":
            ranking_agreement,

        # ------------------------------------
        # Overall consistency
        # ------------------------------------

        "overall_consistency":
            overall_score,

        "overall_consistency_score":
            overall_score,

        "agreement_score":
            overall_score,

        "consistency":
            overall_score,

        "consistency_level":
            consistency_level,

        # ------------------------------------
        # Feature groups
        # ------------------------------------

        "common_features":
            common_display,

        "commonFeatures":
            common_display,

        "shap_only":
            shap_only_display,

        "shap_only_features":
            shap_only_display,

        "shapOnly":
            shap_only_display,

        "lime_only":
            lime_only_display,

        "lime_only_features":
            lime_only_display,

        "limeOnly":
            lime_only_display,

        # ------------------------------------
        # Complete normalized feature lists
        # ------------------------------------

        "shap_features":
            shap_display,

        "lime_features":
            lime_display,

        "shap_feature_names":
            shap_display,

        "lime_feature_names":
            lime_display
    }


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def calculate_agreement(
    shap_results,
    lime_results,
    top_k=5,
    disease=None
):
    """
    Backward-compatible wrapper.

    Existing app.py code can continue calling:

        calculate_agreement(
            shap,
            lime,
            top_k=5,
            disease="diabetes"
        )
    """

    return calculate_shap_lime_agreement(

        shap_results,

        lime_results,

        top_k=top_k,

        disease=disease

    )


# ============================================================
# ADDITIONAL BACKWARD-COMPATIBLE ALIAS
# ============================================================

def get_agreement(
    shap_results,
    lime_results,
    top_k=5,
    disease=None
):
    """
    Alias used by older code versions.
    """

    return calculate_shap_lime_agreement(

        shap_results,

        lime_results,

        top_k=top_k,

        disease=disease

    )


# ============================================================
# SIMPLE TEST
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # Heart
    # --------------------------------------------------------

    heart_shap = [

        {
            "feature":
                "Chest Pain Type",

            "impact":
                0.15
        },

        {
            "feature":
                "Maximum Heart Rate",

            "impact":
                0.08
        },

        {
            "feature":
                "Thalassemia",

            "impact":
                -0.05
        }

    ]

    heart_lime = [

        {
            "feature":
                "cp <= -0.16",

            "impact":
                0.12
        },

        {
            "feature":
                "thalach > 0.71",

            "impact":
                0.06
        },

        {
            "feature":
                "thal <= -0.88",

            "impact":
                -0.03
        }

    ]

    # --------------------------------------------------------
    # Diabetes
    # --------------------------------------------------------

    diabetes_shap = [

        {
            "feature":
                "Polyuria",

            "impact":
                0.19
        },

        {
            "feature":
                "Polydipsia",

            "impact":
                0.09
        },

        {
            "feature":
                "Irritability",

            "impact":
                0.04
        }

    ]

    diabetes_lime = [

        {
            "feature":
                "Polyuria",

            "impact":
                0.45
        },

        {
            "feature":
                "-0.94 < delayed healing <= 1.06",

            "impact":
                0.14
        },

        {
            "feature":
                "Obesity > -0.46",

            "impact":
                -0.13
        }

    ]

    # --------------------------------------------------------
    # CKD
    # --------------------------------------------------------

    ckd_shap = [

        {
            "feature":
                "Hemoglobin",

            "impact":
                0.20
        },

        {
            "feature":
                "Packed Cell Volume",

            "impact":
                0.12
        },

        {
            "feature":
                "Red Blood Cell Count",

            "impact":
                0.08
        }

    ]

    ckd_lime = [

        {
            "feature":
                "hemo > 0.81",

            "impact":
                0.30
        },

        {
            "feature":
                "pcv <= 0.50",

            "impact":
                0.15
        },

        {
            "feature":
                "dm <= -0.69",

            "impact":
                -0.10
        }

    ]

    # --------------------------------------------------------
    # Stroke
    # --------------------------------------------------------

    stroke_shap = [

        {
            "feature":
                "Age",

            "impact":
                0.30
        },

        {
            "feature":
                "Hypertension",

            "impact":
                0.20
        },

        {
            "feature":
                "Average Glucose Level",

            "impact":
                0.15
        }

    ]

    stroke_lime = [

        {
            "feature":
                "age > 0.78",

            "impact":
                0.35
        },

        {
            "feature":
                "hypertension > -0.33",

            "impact":
                0.18
        },

        {
            "feature":
                "avg_glucose_level > 0.17",

            "impact":
                0.12
        }

    ]

    # --------------------------------------------------------
    # Run tests
    # --------------------------------------------------------

    examples = {

        "heart":
            (
                heart_shap,
                heart_lime
            ),

        "diabetes":
            (
                diabetes_shap,
                diabetes_lime
            ),

        "ckd":
            (
                ckd_shap,
                ckd_lime
            ),

        "stroke":
            (
                stroke_shap,
                stroke_lime
            )
    }

    print()
    print("=" * 70)
    print("SHAP-LIME AGREEMENT TEST")
    print("=" * 70)

    for disease_name, values in examples.items():

        shap_data, lime_data = values

        result = calculate_shap_lime_agreement(

            shap_data,

            lime_data,

            top_k=5,

            disease=disease_name

        )

        print()
        print(
            disease_name.upper()
        )

        print(
            "Feature Agreement:",
            result[
                "feature_agreement"
            ]
        )

        print(
            "Direction Agreement:",
            result[
                "direction_agreement"
            ]
        )

        print(
            "Ranking Agreement:",
            result[
                "ranking_agreement"
            ]
        )

        print(
            "Overall Consistency:",
            result[
                "overall_consistency"
            ]
        )

        print(
            "Consistency Level:",
            result[
                "consistency_level"
            ]
        )

        print(
            "Common Features:",
            result[
                "common_features"
            ]
        )

        print(
            "SHAP Only:",
            result[
                "shap_only"
            ]
        )

        print(
            "LIME Only:",
            result[
                "lime_only"
            ]
        )

    print()
    print("=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)