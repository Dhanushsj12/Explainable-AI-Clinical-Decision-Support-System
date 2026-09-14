import os
import itertools
import random

import numpy as np
import pandas as pd

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
    stroke_feature_names
)


# ============================================================
# CONFIGURATION
# ============================================================

RANDOM_SEED = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

MAX_RESULTS = 5
MAX_FEATURES_CHANGED = 3
MAX_TOTAL_CANDIDATES = 2500
MAX_VALUES_PER_FEATURE = 8


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)


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
    "thal"
]


DIABETES_FEATURES = [
    "age",
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
    "obesity"
]


CKD_FEATURES = [
    "age",
    "bp",
    "sg",
    "al",
    "su",
    "rbc",
    "pc",
    "pcc",
    "ba",
    "bgr",
    "bu",
    "sc",
    "sod",
    "pot",
    "hemo",
    "pcv",
    "wbcc",
    "rbcc",
    "htn",
    "dm",
    "cad",
    "appet",
    "pe",
    "ane"
]


STROKE_FEATURES = [
    "gender",
    "age",
    "hypertension",
    "heart_disease",
    "ever_married",
    "work_type",
    "Residence_type",
    "avg_glucose_level",
    "bmi",
    "smoking_status"
]


# ============================================================
# MODEL CONFIGURATION
# ============================================================

MODEL_CONFIG = {

    "heart": {
        "model": heart_model,
        "scaler": heart_scaler,
        "features": HEART_FEATURES
    },

    "diabetes": {
        "model": diabetes_model,
        "scaler": diabetes_scaler,
        "features": DIABETES_FEATURES
    },

    "ckd": {
        "model": ckd_model,
        "scaler": ckd_scaler,
        "features": CKD_FEATURES
    },

    "stroke": {
        "model": stroke_model,
        "scaler": stroke_scaler,
        "features": STROKE_FEATURES,
        "imputer": stroke_imputer
    }

}


EXPECTED_FEATURES = {
    "heart": 13,
    "diabetes": 16,
    "ckd": 24,
    "stroke": 10
}


# ============================================================
# STROKE RAW FEATURE VALUES
#
# The frontend uses numeric category codes.
# They are converted to the original categorical values before
# the trained stroke preprocessing pipeline is applied.
# ============================================================

STROKE_GENDER_VALUES = {
    0: "Female",
    1: "Male",
    2: "Other"
}


STROKE_MARRIED_VALUES = {
    0: "No",
    1: "Yes"
}


STROKE_WORK_VALUES = {
    0: "Private",
    1: "Self-employed",
    2: "Govt_job",
    3: "children",
    4: "Never_worked"
}


STROKE_RESIDENCE_VALUES = {
    0: "Rural",
    1: "Urban"
}


STROKE_SMOKING_VALUES = {
    0: "never smoked",
    1: "formerly smoked",
    2: "smokes",
    3: "Unknown"
}


# ============================================================
# FALLBACK VALUES
# ============================================================

FALLBACK_VALUES = {

    # --------------------------------------------------------
    # Heart
    # --------------------------------------------------------

    "age": [
        30, 35, 40, 45, 50,
        55, 60, 65, 70, 75
    ],

    "sex": [
        0, 1
    ],

    "cp": [
        0, 1, 2, 3
    ],

    "trestbps": [
        100, 110, 120, 130,
        140, 150, 160
    ],

    "chol": [
        150, 170, 190, 210,
        230, 250, 270, 290
    ],

    "fbs": [
        0, 1
    ],

    "restecg": [
        0, 1, 2
    ],

    "thalach": [
        80, 90, 100, 110,
        120, 130, 140, 150,
        160, 170, 180
    ],

    "exang": [
        0, 1
    ],

    "oldpeak": [
        0.0, 0.5, 1.0, 1.5,
        2.0, 2.5, 3.0, 3.5
    ],

    "slope": [
        0, 1, 2
    ],

    "ca": [
        0, 1, 2, 3
    ],

    "thal": [
        0, 1, 2, 3
    ],


    # --------------------------------------------------------
    # Diabetes
    # --------------------------------------------------------

    "gender": [
        0, 1
    ],

    "polyuria": [
        0, 1
    ],

    "polydipsia": [
        0, 1
    ],

    "sudden_weight_loss": [
        0, 1
    ],

    "weakness": [
        0, 1
    ],

    "polyphagia": [
        0, 1
    ],

    "genital_thrush": [
        0, 1
    ],

    "visual_blurring": [
        0, 1
    ],

    "itching": [
        0, 1
    ],

    "irritability": [
        0, 1
    ],

    "delayed_healing": [
        0, 1
    ],

    "partial_paresis": [
        0, 1
    ],

    "muscle_stiffness": [
        0, 1
    ],

    "alopecia": [
        0, 1
    ],

    "obesity": [
        0, 1
    ],


    # --------------------------------------------------------
    # CKD
    # --------------------------------------------------------

    "bp": [
        60, 70, 80, 90,
        100, 110, 120, 140
    ],

    "sg": [
        1.005, 1.010,
        1.015, 1.020,
        1.025
    ],

    "al": [
        0, 1, 2, 3, 4, 5
    ],

    "su": [
        0, 1, 2, 3, 4, 5
    ],

    "rbc": [
        0, 1
    ],

    "pc": [
        0, 1
    ],

    "pcc": [
        0, 1
    ],

    "ba": [
        0, 1
    ],

    "bgr": [
        70, 90, 110, 130,
        150, 170, 200, 250
    ],

    "bu": [
        10, 20, 30, 40,
        50, 60, 80, 100
    ],

    "sc": [
        0.5, 0.7, 1.0, 1.2,
        1.5, 2.0, 3.0, 5.0
    ],

    "sod": [
        125, 130, 135,
        140, 145, 150
    ],

    "pot": [
        3.0, 3.5, 4.0,
        4.5, 5.0, 5.5,
        6.0
    ],

    "hemo": [
        8, 9, 10, 11,
        12, 13, 14, 15,
        16
    ],

    "pcv": [
        20, 25, 30, 35,
        40, 45, 50
    ],

    "wbcc": [
        3000, 5000, 7000,
        9000, 11000, 13000
    ],

    "rbcc": [
        2.5, 3.0, 3.5,
        4.0, 4.5, 5.0,
        5.5, 6.0
    ],

    "htn": [
        0, 1
    ],

    "dm": [
        0, 1
    ],

    "cad": [
        0, 1
    ],

    "appet": [
        0, 1
    ],

    "pe": [
        0, 1
    ],

    "ane": [
        0, 1
    ],


    # --------------------------------------------------------
    # Stroke
    # --------------------------------------------------------

    "gender": [
        0, 1, 2
    ],

    "hypertension": [
        0, 1
    ],

    "heart_disease": [
        0, 1
    ],

    "ever_married": [
        0, 1
    ],

    "work_type": [
        0, 1, 2, 3, 4
    ],

    "Residence_type": [
        0, 1
    ],

    "avg_glucose_level": [
        70, 90, 110, 130,
        150, 170, 200, 250
    ],

    "bmi": [
        18, 20, 22, 24,
        26, 28, 30, 32,
        35, 40
    ],

    "smoking_status": [
        0, 1, 2, 3
    ]

}


# ============================================================
# DISEASE NORMALIZATION
# ============================================================

def normalize_disease(
    disease
):

    if disease is None:
        return "heart"

    value = str(
        disease
    ).strip().lower()

    aliases = {

        "heart": "heart",
        "heart disease": "heart",
        "heart_disease": "heart",

        "diabetes": "diabetes",
        "diabetic": "diabetes",

        "ckd": "ckd",
        "chronic kidney disease": "ckd",
        "chronic_kidney_disease": "ckd",
        "kidney disease": "ckd",

        "stroke": "stroke"

    }

    return aliases.get(
        value,
        value
    )


# ============================================================
# SAFE NUMERIC
# ============================================================

def safe_numeric(
    value
):

    try:

        result = float(
            value
        )

        if np.isfinite(
            result
        ):
            return result

    except (
        TypeError,
        ValueError
    ):
        pass

    return np.nan


# ============================================================
# CLEAN VALUE
# ============================================================

def clean_value(
    value
):

    if value is None:
        return None

    try:

        numeric = float(
            value
        )

        if not np.isfinite(
            numeric
        ):
            return None

        if numeric.is_integer():
            return int(
                numeric
            )

        return round(
            numeric,
            6
        )

    except (
        TypeError,
        ValueError
    ):

        return value


# ============================================================
# LOAD REFERENCE DATASET
# ============================================================

def load_reference_dataset(
    disease
):

    disease = normalize_disease(
        disease
    )

    possible_paths = {

        "heart": [
            os.path.join(
                BASE_DIR,
                "datasets",
                "processed",
                "heart_preprocessed.csv"
            )
        ],

        "diabetes": [
            os.path.join(
                BASE_DIR,
                "datasets",
                "processed",
                "diabetes",
                "x_train.csv"
            )
        ],

        "ckd": [
            os.path.join(
                BASE_DIR,
                "datasets",
                "processed",
                "ckd",
                "x_train.csv"
            )
        ],

        "stroke": [
            os.path.join(
                BASE_DIR,
                "datasets",
                "processed",
                "stroke",
                "x_train.csv"
            )
        ]

    }

    for path in possible_paths.get(
        disease,
        []
    ):

        try:

            if os.path.exists(
                path
            ):

                return pd.read_csv(
                    path
                )

        except Exception:

            continue

    return None


# ============================================================
# BUILD FEATURE DICTIONARY
# ============================================================

def build_feature_dict(
    features,
    disease
):

    disease = normalize_disease(
        disease
    )

    feature_names = MODEL_CONFIG[
        disease
    ][
        "features"
    ]

    # --------------------------------------------------------
    # Dictionary input
    # --------------------------------------------------------

    if isinstance(
        features,
        dict
    ):

        result = {}

        for feature in feature_names:

            if feature in features:

                result[
                    feature
                ] = features[
                    feature
                ]

            elif (
                feature == "Residence_type"
                and
                "residence_type" in features
            ):

                result[
                    feature
                ] = features[
                    "residence_type"
                ]

            else:

                result[
                    feature
                ] = None

        return result

    # --------------------------------------------------------
    # Ordered list / tuple / numpy array
    # --------------------------------------------------------

    if isinstance(
        features,
        (
            list,
            tuple,
            np.ndarray
        )
    ):

        values = list(
            features
        )

        if len(values) != len(
            feature_names
        ):

            raise ValueError(
                f"{disease} requires exactly "
                f"{len(feature_names)} features, "
                f"but received {len(values)}."
            )

        return dict(
            zip(
                feature_names,
                values
            )
        )

    raise ValueError(
        "Features must be a dictionary, list, "
        "tuple, or numpy array."
    )


# ============================================================
# STROKE CATEGORY NORMALIZATION
# ============================================================

def stroke_category_value(
    feature,
    value
):

    if value is None:
        return value

    # --------------------------------------------------------
    # Already textual
    # --------------------------------------------------------

    if isinstance(
        value,
        str
    ):

        text = value.strip()

        if feature == "gender":

            lowered = text.lower()

            if lowered == "male":
                return "Male"

            if lowered == "female":
                return "Female"

            if lowered == "other":
                return "Other"

        if feature == "ever_married":

            lowered = text.lower()

            if lowered == "yes":
                return "Yes"

            if lowered == "no":
                return "No"

        if feature == "work_type":

            aliases = {
                "private": "Private",
                "self-employed": "Self-employed",
                "self employed": "Self-employed",
                "govt_job": "Govt_job",
                "government job": "Govt_job",
                "children": "children",
                "never worked": "Never_worked",
                "never_worked": "Never_worked"
            }

            return aliases.get(
                text.lower(),
                text
            )

        if feature == "Residence_type":

            lowered = text.lower()

            if lowered == "urban":
                return "Urban"

            if lowered == "rural":
                return "Rural"

        if feature == "smoking_status":

            aliases = {
                "never smoked": "never smoked",
                "formerly smoked": "formerly smoked",
                "smokes": "smokes",
                "currently smokes": "smokes",
                "unknown": "Unknown"
            }

            return aliases.get(
                text.lower(),
                text
            )

        return text

    # --------------------------------------------------------
    # Numeric category codes
    # --------------------------------------------------------

    try:

        number = int(
            float(value)
        )

    except (
        TypeError,
        ValueError
    ):

        return value

    if feature == "gender":

        return STROKE_GENDER_VALUES.get(
            number,
            "Other"
        )

    if feature == "ever_married":

        return STROKE_MARRIED_VALUES.get(
            number,
            "No"
        )

    if feature == "work_type":

        return STROKE_WORK_VALUES.get(
            number,
            "Private"
        )

    if feature == "Residence_type":

        return STROKE_RESIDENCE_VALUES.get(
            number,
            "Rural"
        )

    if feature == "smoking_status":

        return STROKE_SMOKING_VALUES.get(
            number,
            "Unknown"
        )

    return value


# ============================================================
# STROKE PREPROCESSING
# ============================================================

def preprocess_stroke_patient(
    patient
):

    raw = dict(
        patient
    )

    # --------------------------------------------------------
    # Normalize categorical fields BEFORE encoding.
    # --------------------------------------------------------

    for feature in [
        "gender",
        "ever_married",
        "work_type",
        "Residence_type",
        "smoking_status"
    ]:

        raw[
            feature
        ] = stroke_category_value(
            feature,
            raw.get(
                feature
            )
        )

    # --------------------------------------------------------
    # Numeric fields
    # --------------------------------------------------------

    numerical_columns = [
        "age",
        "hypertension",
        "heart_disease",
        "avg_glucose_level",
        "bmi"
    ]

    categorical_columns = [
        "gender",
        "ever_married",
        "work_type",
        "Residence_type",
        "smoking_status"
    ]

    # --------------------------------------------------------
    # Raw DataFrame
    # --------------------------------------------------------

    df = pd.DataFrame(
        [raw],
        columns=STROKE_FEATURES
    )

    # --------------------------------------------------------
    # Numeric conversion
    # --------------------------------------------------------

    for column in numerical_columns:

        df[
            column
        ] = pd.to_numeric(
            df[
                column
            ],
            errors="coerce"
        )

    # --------------------------------------------------------
    # Impute numerical columns.
    #
    # Important:
    # categorical columns must NOT be passed through the
    # numerical imputer.
    # --------------------------------------------------------

    try:

        transformed_numeric = (
            stroke_imputer.transform(
                df[
                    numerical_columns
                ]
            )
        )

        df[
            numerical_columns
        ] = transformed_numeric

    except Exception:

        for column in numerical_columns:

            if df[
                column
            ].isnull().any():

                median = df[
                    column
                ].median()

                if pd.isna(
                    median
                ):

                    median = 0.0

                df[
                    column
                ] = df[
                    column
                ].fillna(
                    median
                )

    # --------------------------------------------------------
    # Safe categorical fallback.
    # --------------------------------------------------------

    for column in categorical_columns:

        if df[
            column
        ].isnull().any():

            df[
                column
            ] = df[
                column
            ].fillna(
                "Unknown"
            )

    # --------------------------------------------------------
    # One-hot encoding.
    # --------------------------------------------------------

    encoded = pd.get_dummies(
        df,
        columns=categorical_columns,
        drop_first=False
    )

    # --------------------------------------------------------
    # Match EXACT model training feature names.
    # --------------------------------------------------------

    encoded = encoded.reindex(
        columns=stroke_feature_names,
        fill_value=0
    )

    encoded = encoded[
        stroke_feature_names
    ]

    encoded = encoded.astype(
        float
    )

    # --------------------------------------------------------
    # Scaling.
    # --------------------------------------------------------

    scaled = stroke_scaler.transform(
        encoded
    )

    return scaled


# ============================================================
# BUILD MODEL FRAME
# ============================================================

def build_model_frame(
    patient,
    disease
):

    disease = normalize_disease(
        disease
    )

    feature_names = MODEL_CONFIG[
        disease
    ][
        "features"
    ]

    row = {}

    for feature in feature_names:

        value = patient.get(
            feature
        )

        if (
            value is None
            and
            feature == "Residence_type"
        ):

            value = patient.get(
                "residence_type"
            )

        row[
            feature
        ] = value

    return pd.DataFrame(
        [row],
        columns=feature_names
    )


# ============================================================
# PREPARE MODEL INPUT
# ============================================================

def prepare_model_input(
    patient,
    disease
):

    disease = normalize_disease(
        disease
    )

    if disease == "stroke":

        return preprocess_stroke_patient(
            patient
        )

    config = MODEL_CONFIG[
        disease
    ]

    df = build_model_frame(
        patient,
        disease
    )

    for column in df.columns:

        df[
            column
        ] = pd.to_numeric(
            df[
                column
            ],
            errors="coerce"
        )

    # --------------------------------------------------------
    # Fill missing values safely.
    # --------------------------------------------------------

    for column in df.columns:

        if df[
            column
        ].isnull().any():

            median = df[
                column
            ].median()

            if pd.isna(
                median
            ):

                median = 0.0

            df[
                column
            ] = df[
                column
            ].fillna(
                median
            )

    return df


# ============================================================
# PREDICT PATIENT
# ============================================================

def predict_patient(
    patient,
    disease
):

    disease = normalize_disease(
        disease
    )

    if disease not in MODEL_CONFIG:

        raise ValueError(
            "Unsupported disease: "
            + str(disease)
        )

    config = MODEL_CONFIG[
        disease
    ]

    model = config[
        "model"
    ]

    scaler = config[
        "scaler"
    ]

    model_input = prepare_model_input(
        patient,
        disease
    )

    scaled = scaler.transform(
        model_input
    )

    prediction = int(
        model.predict(
            scaled
        )[0]
    )

    try:

        probability = float(
            model.predict_proba(
                scaled
            )[0][1]
        )

    except Exception:

        probability = (
            1.0
            if prediction == 1
            else 0.0
        )

    return (
        prediction,
        probability
    )


# ============================================================
# REFERENCE VALUES
# ============================================================

def get_reference_values(
    disease,
    feature,
    current_value
):

    disease = normalize_disease(
        disease
    )

    values = []

    # --------------------------------------------------------
    # STROKE
    #
    # Stroke x_train is normally already one-hot encoded.
    # Therefore raw categorical features such as work_type and
    # smoking_status cannot reliably be obtained from its
    # columns. Use the raw category search space below.
    # --------------------------------------------------------

    if disease == "stroke":

        if feature == "gender":

            values = [
                0,
                1,
                2
            ]

        elif feature == "age":

            values = [
                30, 35, 40, 45,
                50, 55, 60, 65,
                70, 75, 80
            ]

        elif feature in [
            "hypertension",
            "heart_disease",
            "ever_married",
            "Residence_type"
        ]:

            values = list(
                FALLBACK_VALUES.get(
                    feature,
                    [0, 1]
                )
            )

        elif feature == "work_type":

            values = [
                0,
                1,
                2,
                3,
                4
            ]

        elif feature == "smoking_status":

            values = [
                0,
                1,
                2,
                3
            ]

        elif feature == "avg_glucose_level":

            values = [
                70,
                90,
                110,
                130,
                150,
                170,
                200,
                250,
                300
            ]

        elif feature == "bmi":

            values = [
                18,
                20,
                22,
                24,
                26,
                28,
                30,
                32,
                35,
                40
            ]

        else:

            values = list(
                FALLBACK_VALUES.get(
                    feature,
                    []
                )
            )

        current_numeric = safe_numeric(
            current_value
        )

        if np.isfinite(
            current_numeric
        ):

            values.append(
                current_numeric
            )

        cleaned = []

        for value in values:

            numeric = safe_numeric(
                value
            )

            if np.isfinite(
                numeric
            ):

                cleaned.append(
                    numeric
                )

        return sorted(
            set(
                cleaned
            )
        )

    # --------------------------------------------------------
    # Other diseases
    # --------------------------------------------------------

    df = load_reference_dataset(
        disease
    )

    if df is not None:

        column = feature

        if (
            column not in df.columns
            and
            feature == "Residence_type"
            and
            "residence_type" in df.columns
        ):

            column = "residence_type"

        if column in df.columns:

            series = pd.to_numeric(
                df[
                    column
                ],
                errors="coerce"
            ).dropna()

            if len(series) > 0:

                unique_values = sorted(
                    set(
                        float(value)
                        for value in series.tolist()
                        if np.isfinite(
                            float(value)
                        )
                    )
                )

                if len(unique_values) <= 20:

                    values.extend(
                        unique_values
                    )

                else:

                    quantiles = np.linspace(
                        0.05,
                        0.95,
                        9
                    )

                    for q in quantiles:

                        values.append(
                            float(
                                series.quantile(
                                    q
                                )
                            )
                        )

    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------

    if not values:

        values = list(
            FALLBACK_VALUES.get(
                feature,
                []
            )
        )

    # --------------------------------------------------------
    # Current value
    # --------------------------------------------------------

    current_numeric = safe_numeric(
        current_value
    )

    if np.isfinite(
        current_numeric
    ):

        values.append(
            current_numeric
        )

    # --------------------------------------------------------
    # Clean
    # --------------------------------------------------------

    cleaned = []

    for value in values:

        numeric = safe_numeric(
            value
        )

        if np.isfinite(
            numeric
        ):

            cleaned.append(
                numeric
            )

    cleaned = sorted(
        set(
            cleaned
        )
    )

    # --------------------------------------------------------
    # Limit candidate values.
    # --------------------------------------------------------

    if len(cleaned) > MAX_VALUES_PER_FEATURE:

        if np.isfinite(
            current_numeric
        ):

            cleaned = sorted(
                cleaned,
                key=lambda value:
                    abs(
                        value -
                        current_numeric
                    )
            )[
                :MAX_VALUES_PER_FEATURE
            ]

        else:

            cleaned = cleaned[
                :MAX_VALUES_PER_FEATURE
            ]

        cleaned = sorted(
            cleaned
        )

    return cleaned


# ============================================================
# CHANGE MAGNITUDE
# ============================================================

def calculate_change_magnitude(
    original,
    new_value
):

    try:

        old = float(
            original
        )

        new = float(
            new_value
        )

        # Binary changes.
        if (
            old in [0, 1]
            and
            new in [0, 1]
        ):

            return (
                0.0
                if old == new
                else 1.0
            )

        denominator = max(
            abs(old),
            1.0
        )

        return abs(
            new - old
        ) / denominator

    except (
        TypeError,
        ValueError
    ):

        return (
            0.0
            if str(original) ==
            str(new_value)
            else 1.0
        )


# ============================================================
# CANDIDATE VALUES
# ============================================================

def candidate_values_for_feature(
    patient,
    disease,
    feature
):

    original = patient.get(
        feature
    )

    values = get_reference_values(
        disease,
        feature,
        original
    )

    result = []

    for value in values:

        try:

            if original is not None:

                if (
                    abs(
                        float(value)
                        -
                        float(original)
                    ) < 1e-12
                ):

                    continue

        except (
            TypeError,
            ValueError
        ):

            if str(value) == str(
                original
            ):

                continue

        result.append(
            value
        )

    return result


# ============================================================
# SINGLE-FEATURE CANDIDATES
# ============================================================

def generate_single_feature_candidates(
    patient,
    disease
):

    feature_names = MODEL_CONFIG[
        disease
    ][
        "features"
    ]

    candidates = []

    for feature in feature_names:

        values = candidate_values_for_feature(
            patient,
            disease,
            feature
        )

        for value in values:

            candidates.append({

                feature: {

                    "old":
                        clean_value(
                            patient.get(
                                feature
                            )
                        ),

                    "new":
                        clean_value(
                            value
                        ),

                    "normalized_change":
                        round(
                            calculate_change_magnitude(
                                patient.get(
                                    feature
                                ),
                                value
                            ),
                            6
                        )

                }

            })

    return candidates


# ============================================================
# MULTI-FEATURE CANDIDATES
# ============================================================

def generate_multi_feature_candidates(
    patient,
    disease,
    max_features_changed=3,
    max_candidates=MAX_TOTAL_CANDIDATES
):

    feature_names = MODEL_CONFIG[
        disease
    ][
        "features"
    ]

    max_features_changed = max(
        1,
        min(
            int(
                max_features_changed
            ),
            MAX_FEATURES_CHANGED
        )
    )

    feature_candidates = {}

    # --------------------------------------------------------
    # Candidate values for every feature.
    # --------------------------------------------------------

    for feature in feature_names:

        values = candidate_values_for_feature(
            patient,
            disease,
            feature
        )

        original = patient.get(
            feature
        )

        # ----------------------------------------------------
        # Keep values close to current value first.
        # ----------------------------------------------------

        try:

            values = sorted(
                values,
                key=lambda value:
                    abs(
                        float(value)
                        -
                        float(original)
                    )
                if original is not None
                else 0
            )

        except Exception:

            pass

        feature_candidates[
            feature
        ] = values[
            :MAX_VALUES_PER_FEATURE
        ]

    candidates = []

    # --------------------------------------------------------
    # One, two and three feature changes.
    # --------------------------------------------------------

    for number_of_changes in range(
        1,
        max_features_changed + 1
    ):

        for selected_features in itertools.combinations(
            feature_names,
            number_of_changes
        ):

            value_lists = [

                feature_candidates.get(
                    feature,
                    []
                )

                for feature
                in selected_features

            ]

            if any(
                len(values) == 0
                for values in value_lists
            ):

                continue

            for candidate_values in itertools.product(
                *value_lists
            ):

                changes = {}
                valid = True

                for feature, new_value in zip(
                    selected_features,
                    candidate_values
                ):

                    original = patient.get(
                        feature
                    )

                    try:

                        if (
                            original is not None
                            and
                            abs(
                                float(new_value)
                                -
                                float(original)
                            ) < 1e-12
                        ):

                            valid = False
                            break

                    except (
                        TypeError,
                        ValueError
                    ):

                        if str(new_value) == str(
                            original
                        ):

                            valid = False
                            break

                    changes[
                        feature
                    ] = {

                        "old":
                            clean_value(
                                original
                            ),

                        "new":
                            clean_value(
                                new_value
                            ),

                        "normalized_change":
                            calculate_change_magnitude(
                                original,
                                new_value
                            )

                    }

                if not valid:
                    continue

                candidates.append(
                    changes
                )

                if len(
                    candidates
                ) >= max_candidates:

                    return candidates

    return candidates


# ============================================================
# CANDIDATE DISTANCE
# ============================================================

def candidate_distance(
    changes
):

    if not changes:
        return 0.0

    total = 0.0

    for item in changes.values():

        if not isinstance(
            item,
            dict
        ):

            continue

        magnitude = item.get(
            "normalized_change",
            0.0
        )

        try:

            total += float(
                magnitude
            )

        except (
            TypeError,
            ValueError
        ):

            total += 1.0

    return total


# ============================================================
# BUILD CHANGED PATIENT
# ============================================================

def apply_changes(
    patient,
    changes
):

    result = dict(
        patient
    )

    for feature, new_value in changes.items():

        result[
            feature
        ] = new_value

    return result


# ============================================================
# EVALUATE CANDIDATE
# ============================================================

def evaluate_candidate(
    patient,
    changes,
    disease,
    original_prediction
):

    candidate_patient = apply_changes(
        patient,
        {
            feature:
                details[
                    "new"
                ]
            for feature, details
            in changes.items()
        }
    )

    try:

        prediction, probability = (
            predict_patient(
                candidate_patient,
                disease
            )
        )

    except Exception as error:

        # Keep search running if one malformed candidate
        # cannot be processed.
        print(
            "Counterfactual candidate error:",
            repr(error)
        )

        return None

    # --------------------------------------------------------
    # Counterfactual must cross the decision boundary.
    # --------------------------------------------------------

    if prediction == original_prediction:

        return None

    number_of_changes = len(
        changes
    )

    normalized_change = candidate_distance(
        changes
    )

    return {

        "changes":
            changes,

        "prediction":
            prediction,

        "prediction_class":
            prediction,

        "probability":
            probability,

        "new_probability":
            probability,

        "number_of_changes":
            number_of_changes,

        "normalized_change":
            round(
                normalized_change,
                4
            ),

        "distance":
            round(
                normalized_change,
                4
            )

    }


# ============================================================
# SORT COUNTERFACTUALS
# ============================================================

def sort_counterfactuals(
    counterfactuals
):

    return sorted(

        counterfactuals,

        key=lambda item: (

            item.get(
                "number_of_changes",
                999
            ),

            item.get(
                "normalized_change",
                999999
            ),

            -float(
                item.get(
                    "probability",
                    0
                )
            )

        )

    )


# ============================================================
# FIND COUNTERFACTUALS
# ============================================================

def find_counterfactuals(
    patient,
    disease="heart",
    max_results=5,
    max_features_changed=3
):

    disease = normalize_disease(
        disease
    )

    if disease not in MODEL_CONFIG:

        raise ValueError(
            "Unsupported disease: "
            + str(disease)
        )

    if max_results is None:

        max_results = MAX_RESULTS

    max_results = max(
        1,
        int(
            max_results
        )
    )

    if max_features_changed is None:

        max_features_changed = (
            MAX_FEATURES_CHANGED
        )

    max_features_changed = max(
        1,
        min(
            int(
                max_features_changed
            ),
            MAX_FEATURES_CHANGED
        )
    )

    # --------------------------------------------------------
    # Convert input into exact feature dictionary.
    # --------------------------------------------------------

    patient_dict = build_feature_dict(
        patient,
        disease
    )

    # --------------------------------------------------------
    # Original prediction.
    # --------------------------------------------------------

    original_prediction, original_probability = (
        predict_patient(
            patient_dict,
            disease
        )
    )

    print()
    print(
        "=" * 60
    )
    print(
        "MULTI-FEATURE COUNTERFACTUAL SEARCH"
    )
    print(
        "=" * 60
    )

    print(
        "Disease:",
        disease
    )

    print(
        "Original Prediction:",
        original_prediction
    )

    print(
        "Original Probability:",
        round(
            original_probability * 100,
            2
        ),
        "%"
    )

    print(
        "Target Class:",
        (
            1
            if original_prediction == 0
            else 0
        )
    )

    print(
        "Maximum Feature Changes:",
        max_features_changed
    )

    # --------------------------------------------------------
    # Generate candidates.
    # --------------------------------------------------------

    candidates = generate_multi_feature_candidates(
        patient_dict,
        disease,
        max_features_changed=max_features_changed,
        max_candidates=MAX_TOTAL_CANDIDATES
    )

    print(
        "Generated Candidates:",
        len(candidates)
    )

    # --------------------------------------------------------
    # Evaluate.
    # --------------------------------------------------------

    found = []

    seen = set()

    total_tested = 0

    for changes in candidates:

        total_tested += 1

        evaluated = evaluate_candidate(
            patient_dict,
            changes,
            disease,
            original_prediction
        )

        if evaluated is None:

            continue

        signature = tuple(

            (
                feature,
                str(
                    details.get(
                        "old"
                    )
                ),
                str(
                    details.get(
                        "new"
                    )
                )

            )

            for feature, details
            in sorted(
                changes.items()
            )

        )

        if signature in seen:

            continue

        seen.add(
            signature
        )

        found.append(
            evaluated
        )

    print(
        "Candidates Tested:",
        total_tested
    )

    print(
        "Valid Counterfactuals:",
        len(found)
    )

    # --------------------------------------------------------
    # Sort and return best results.
    # --------------------------------------------------------

    found = sort_counterfactuals(
        found
    )

    found = found[
        :max_results
    ]

    print(
        "Returning:",
        len(found),
        "counterfactuals"
    )

    print(
        "=" * 60
    )

    return (
        original_prediction,
        original_probability,
        found
    )


# ============================================================
# DISEASE-SPECIFIC WRAPPERS
# ============================================================

def find_heart_counterfactuals(
    features,
    max_results=5
):

    return find_counterfactuals(
        features,
        disease="heart",
        max_results=max_results
    )


def find_diabetes_counterfactuals(
    features,
    max_results=5
):

    return find_counterfactuals(
        features,
        disease="diabetes",
        max_results=max_results
    )


def find_ckd_counterfactuals(
    features,
    max_results=5
):

    return find_counterfactuals(
        features,
        disease="ckd",
        max_results=max_results
    )


def find_stroke_counterfactuals(
    features,
    max_results=5
):

    return find_counterfactuals(
        features,
        disease="stroke",
        max_results=max_results
    )


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def build_heart_counterfactual_input(
    features
):

    return build_feature_dict(
        features,
        "heart"
    )


# ============================================================
# PREDICTION TEXT
# ============================================================

def get_prediction_text(
    disease,
    prediction
):

    disease = normalize_disease(
        disease
    )

    try:

        prediction = int(
            prediction
        )

    except (
        TypeError,
        ValueError
    ):

        return str(
            prediction
        )

    if disease == "heart":

        return (
            "Heart Disease"
            if prediction == 1
            else
            "No Heart Disease"
        )

    if disease == "diabetes":

        return (
            "Diabetes"
            if prediction == 1
            else
            "No Diabetes"
        )

    if disease == "ckd":

        return (
            "Chronic Kidney Disease"
            if prediction == 1
            else
            "No Chronic Kidney Disease"
        )

    if disease == "stroke":

        return (
            "Stroke Risk"
            if prediction == 1
            else
            "No Stroke Risk"
        )

    return str(
        prediction
    )


# ============================================================
# NORMALIZE COUNTERFACTUALS
# ============================================================

def normalize_counterfactuals(
    counterfactuals,
    disease="heart"
):

    if not isinstance(
        counterfactuals,
        list
    ):

        return []

    disease = normalize_disease(
        disease
    )

    normalized = []

    for cf in counterfactuals:

        if not isinstance(
            cf,
            dict
        ):

            continue

        prediction = cf.get(
            "prediction",
            cf.get(
                "prediction_class"
            )
        )

        try:

            prediction_int = int(
                prediction
            )

        except (
            TypeError,
            ValueError
        ):

            prediction_int = prediction

        changes = cf.get(
            "changes",
            {}
        )

        normalized_changes = {}

        if isinstance(
            changes,
            dict
        ):

            for feature, value in changes.items():

                if isinstance(
                    value,
                    dict
                ):

                    old_value = value.get(
                        "old",
                        value.get(
                            "original",
                            value.get(
                                "from"
                            )
                        )
                    )

                    new_value = value.get(
                        "new",
                        value.get(
                            "counterfactual",
                            value.get(
                                "to"
                            )
                        )
                    )

                    normalized_changes[
                        feature
                    ] = {

                        "old":
                            clean_value(
                                old_value
                            ),

                        "new":
                            clean_value(
                                new_value
                            )

                    }

                else:

                    normalized_changes[
                        feature
                    ] = {

                        "old":
                            None,

                        "new":
                            clean_value(
                                value
                            )

                    }

        probability = cf.get(
            "probability",
            cf.get(
                "new_probability",
                0
            )
        )

        # ----------------------------------------------------
        # Keep probability in the backend's normal
        # 0-1 representation.
        # ----------------------------------------------------

        try:

            probability = float(
                probability
            )

        except (
            TypeError,
            ValueError
        ):

            probability = 0.0

        normalized_change = cf.get(
            "normalized_change",
            cf.get(
                "distance",
                0
            )
        )

        try:

            normalized_change = float(
                normalized_change
            )

        except (
            TypeError,
            ValueError
        ):

            normalized_change = 0.0

        number_of_changes = cf.get(
            "number_of_changes",
            len(
                normalized_changes
            )
        )

        try:

            number_of_changes = int(
                number_of_changes
            )

        except (
            TypeError,
            ValueError
        ):

            number_of_changes = len(
                normalized_changes
            )

        normalized.append({

            "changes":
                normalized_changes,

            "prediction":
                prediction_int,

            "prediction_class":
                prediction_int,

            "prediction_text":
                get_prediction_text(
                    disease,
                    prediction_int
                ),

            "probability":
                probability,

            "new_probability":
                probability,

            "number_of_changes":
                number_of_changes,

            "normalized_change":
                round(
                    normalized_change,
                    4
                ),

            "distance":
                round(
                    normalized_change,
                    4
                )

        })

    return normalized


# ============================================================
# HIGH-LEVEL EXPLANATION
# ============================================================

def generate_counterfactual_explanation(
    features,
    disease,
    max_results=5
):

    disease = normalize_disease(
        disease
    )

    (
        original_prediction,
        original_probability,
        counterfactuals
    ) = find_counterfactuals(

        features,

        disease=disease,

        max_results=max_results

    )

    normalized = normalize_counterfactuals(
        counterfactuals,
        disease=disease
    )

    return {

        "disease":
            disease,

        "original_prediction":
            original_prediction,

        "original_prediction_class":
            original_prediction,

        "original_prediction_text":
            get_prediction_text(
                disease,
                original_prediction
            ),

        "original_probability":
            round(
                original_probability * 100,
                2
            ),

        "counterfactuals":
            normalized,

        "count":
            len(
                normalized
            )

    }


# ============================================================
# SIMPLE API
# ============================================================

def get_counterfactuals(
    result
):

    if not isinstance(
        result,
        dict
    ):

        return []

    disease = normalize_disease(
        result.get(
            "disease",
            "heart"
        )
    )

    features = result.get(
        "features"
    )

    if features is None:

        return []

    try:

        explanation = (
            generate_counterfactual_explanation(
                features,
                disease,
                max_results=MAX_RESULTS
            )
        )

        return explanation[
            "counterfactuals"
        ]

    except Exception as error:

        print(
            "Counterfactual API error:",
            repr(error)
        )

        return []


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    print()
    print(
        "=" * 70
    )
    print(
        "MULTI-DISEASE COUNTERFACTUAL ENGINE"
    )
    print(
        "=" * 70
    )

    print(
        "Supported diseases:"
    )

    for disease in MODEL_CONFIG:

        print(
            " -",
            disease
        )

    print(
        "=" * 70
    )

    print(
        "Counterfactual engine loaded successfully."
    )

    print(
        "Functions available:"
    )

    print(
        " - find_heart_counterfactuals()"
    )

    print(
        " - find_diabetes_counterfactuals()"
    )

    print(
        " - find_ckd_counterfactuals()"
    )

    print(
        " - find_stroke_counterfactuals()"
    )

    print(
        " - find_counterfactuals(features, disease)"
    )

    print(
        "=" * 70
    )