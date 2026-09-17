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
    stroke_feature_names,
    stroke_threshold
)


# ============================================================
# CONFIGURATION
# ============================================================

RANDOM_SEED = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

MAX_RESULTS = 5
MAX_FEATURES_CHANGED = 2
MAX_TOTAL_CANDIDATES = 500
MAX_VALUES_PER_FEATURE = 8


# ============================================================
# IMMUTABLE FEATURES
# ============================================================
# Features that should not be altered when generating a
# counterfactual for a patient.  These are treated as fixed
# patient attributes during the search.
IMMUTABLE_FEATURES = {
    "heart": {"age", "sex"},
    "diabetes": {"age",},
    "ckd": {"age"},
    "stroke": {"age", "gender"},
}
# ============================================================
# PREFERRED COUNTERFACTUAL FEATURES
# ============================================================

PREFERRED_FEATURES = {
    "heart": [
        "trestbps",
        "chol",
        "fbs",
        "thalach",
        "exang",
        "oldpeak",
        "cp",
        "restecg",
        "slope",
        "ca",
        "thal",
    ],

    "diabetes": [
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
    ],

    "ckd": [
        "al",
        "su",
        "sg",
        "bgr",
        "bu",
        "sc",
        "sod",
        "pot",
        "hemo",
        "pcv",
        "wbcc",
        "rbcc",
        "rbc",
        "pc",
        "pcc",
        "ba",
        "appet",
        "pe",
        "ane",
        "bp",
    ],

    "stroke": [
        "smoking_status",
        "hypertension",
        "avg_glucose_level",
        "bmi",
    ],
}
# ============================================================
# DOMAIN BOUNDS
# ============================================================
# Protect counterfactual search from numerical values outside
# the ordinary ranges represented by the project datasets.

DOMAIN_BOUNDS = {
    "age": (18.0, 100.0),

    # Heart
    "trestbps": (80.0, 220.0),
    "chol": (80.0, 650.0),
    "thalach": (40.0, 220.0),
    "oldpeak": (-2.0, 8.0),

    # CKD
    "bp": (40.0, 240.0),
    "sg": (1.0, 1.1),
    "bgr": (40.0, 500.0),
    "bu": (1.0, 200.0),
    "sc": (0.1, 20.0),
    "sod": (100.0, 180.0),
    "pot": (1.5, 10.0),
    "hemo": (3.0, 20.0),
    "pcv": (10.0, 70.0),
    "wbcc": (1000.0, 30000.0),
    "rbcc": (1.0, 10.0),

    # Stroke
    "avg_glucose_level": (40.0, 500.0),
    "bmi": (10.0, 70.0),
}
# ============================================================
# CATEGORICAL / BINARY FEATURES
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
        "rbc",
        "pc",
        "pcc",
        "ba",
        "htn",
        "dm",
        "cad",
        "appet",
        "pe",
        "ane",
    },

    "stroke": {
        "gender",
        "hypertension",
        "heart_disease",
        "ever_married",
        "work_type",
        "Residence_type",
        "smoking_status",
    },
}
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

    config = MODEL_CONFIG[
        disease
    ]

    feature_names = config[
        "features"
    ]

    row = {}

    # Build the canonical raw feature dictionary first.
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

        row[feature] = value

    df = pd.DataFrame(
        [row],
        columns=feature_names
    )

    # --------------------------------------------------------
    # Some of the stored Diabetes preprocessing objects were
    # fitted with human-readable column names (for example
    # ``Age`` and ``Alopecia``), while the XAI/CF layer uses
    # canonical snake_case names.  Align to the scaler's exact
    # training names before calling transform().
    # --------------------------------------------------------
    scaler = config.get(
        "scaler"
    )

    fitted_names = getattr(
        scaler,
        "feature_names_in_",
        None
    )

    if fitted_names is not None:

        alias_map = {
            "age": "Age",
            "gender": "Gender",
            "polyuria": "Polyuria",
            "polydipsia": "Polydipsia",
            "sudden_weight_loss": "Sudden weight loss",
            "weakness": "Weakness",
            "polyphagia": "Polyphagia",
            "genital_thrush": "Genital thrush",
            "visual_blurring": "Visual blurring",
            "itching": "Itching",
            "irritability": "Irritability",
            "delayed_healing": "Delayed healing",
            "partial_paresis": "Partial paresis",
            "muscle_stiffness": "Muscle stiffness",
            "alopecia": "Alopecia",
            "obesity": "Obesity",
        }

        # Prefer the exact fitted name where a canonical alias
        # exists; otherwise keep the original canonical column.
        rename = {}
        for canonical, human in alias_map.items():
            if canonical in df.columns and human in fitted_names:
                rename[canonical] = human

        if rename:
            df = df.rename(
                columns=rename
            )

        # Reindex to the exact feature order used during fit.
        df = df.reindex(
            columns=list(fitted_names),
            fill_value=np.nan
        )

    return df


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

    # ------------------------------------------------------------
    # Stroke MUST use the exact same preprocessing and decision
    # threshold as the production prediction pipeline.
    #
    # preprocess_stroke_patient() already performs:
    # raw categorical normalization -> imputation -> one-hot
    # encoding -> exact feature ordering -> scaling.
    # Do NOT scale Stroke a second time.
    # ------------------------------------------------------------
    if disease == "stroke":

        model_input = preprocess_stroke_patient(
            patient
        )

        try:
            probability = float(
                model.predict_proba(
                    model_input
                )[0][1]
            )
        except Exception:
            prediction_raw = int(
                model.predict(
                    model_input
                )[0]
            )
            probability = (
                1.0
                if prediction_raw == 1
                else 0.0
            )

        prediction = int(
            probability >= stroke_threshold
        )

        return (
            prediction,
            probability
        )

    # ------------------------------------------------------------
    # Heart / Diabetes / CKD:
    # Follow their existing production path:
    # raw feature frame -> numeric conversion -> scaler -> model.
    # ------------------------------------------------------------
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
    new_value,
    disease=None,
    feature=None
):

    # ------------------------------------------------------------
    # Categorical/binary changes:
    # One state transition = one unit of change.
    # ------------------------------------------------------------
    if (
        disease is not None
        and
        feature is not None
        and
        feature in CATEGORICAL_FEATURES.get(
            normalize_disease(disease),
            set()
        )
    ):

        try:
            old = float(original)
            new = float(new_value)

            return (
                0.0
                if abs(old - new) < 1e-12
                else 1.0
            )

        except (
            TypeError,
            ValueError
        ):

            return (
                0.0
                if str(original) == str(new_value)
                else 1.0
            )

    # ------------------------------------------------------------
    # Numerical changes:
    # Normalize using the reference distribution when available.
    # This prevents values like:
    #     SG 1.020 -> 1.010
    # from being treated with the same scale as a large laboratory
    # measurement change.
    # ------------------------------------------------------------
    try:

        old = float(
            original
        )

        new = float(
            new_value
        )

        if (
            not np.isfinite(old)
            or
            not np.isfinite(new)
        ):
            raise ValueError

        if abs(old - new) < 1e-12:
            return 0.0

        if (
            disease is not None
            and
            feature is not None
        ):

            stats = _reference_numeric_stats(
                disease,
                feature
            )

            if stats is not None:

                scale = max(
                    stats.get(
                        "q90",
                        0.0
                    )
                    -
                    stats.get(
                        "q10",
                        0.0
                    ),
                    1e-9
                )

                return abs(
                    new - old
                ) / scale

        # Fallback when reference statistics are unavailable.
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


def feature_is_immutable(
    disease,
    feature
):
    disease = normalize_disease(disease)

    return feature in IMMUTABLE_FEATURES.get(
        disease,
        set()
    )


def feature_priority(
    disease,
    feature
):
    disease = normalize_disease(disease)

    preferred = PREFERRED_FEATURES.get(
        disease,
        []
    )

    try:
        index = preferred.index(feature)
        return index
    except ValueError:
        return len(preferred) + 100


def within_domain(
    feature,
    value
):
    numeric = safe_numeric(value)

    if not np.isfinite(numeric):
        return True

    bounds = DOMAIN_BOUNDS.get(
        feature
    )

    if bounds is None:
        return True

    lower, upper = bounds

    return (
        lower <= numeric <= upper
    )


_REFERENCE_STATS_CACHE = {}


def _reference_numeric_stats(
    disease,
    feature
):
    """
    Return robust statistics from the project's reference training
    data. Results are cached because counterfactual search may evaluate
    thousands of candidates.
    """

    disease = normalize_disease(
        disease
    )

    cache_key = (
        disease,
        feature
    )

    if cache_key in _REFERENCE_STATS_CACHE:
        return _REFERENCE_STATS_CACHE[cache_key]

    df = load_reference_dataset(
        disease
    )

    if df is None:
        _REFERENCE_STATS_CACHE[cache_key] = None
        return None

    column = feature

    if (
        column not in df.columns
        and
        feature == "Residence_type"
        and
        "residence_type" in df.columns
    ):
        column = "residence_type"

    if column not in df.columns:
        _REFERENCE_STATS_CACHE[cache_key] = None
        return None

    series = pd.to_numeric(
        df[column],
        errors="coerce"
    ).dropna()

    if len(series) == 0:
        _REFERENCE_STATS_CACHE[cache_key] = None
        return None

    values = series.to_numpy(
        dtype=float
    )

    values = values[
        np.isfinite(values)
    ]

    if len(values) == 0:
        _REFERENCE_STATS_CACHE[cache_key] = None
        return None

    stats = {
        "median": float(
            np.median(values)
        ),
        "q01": float(
            np.quantile(values, 0.01)
        ),
        "q99": float(
            np.quantile(values, 0.99)
        ),
        "q10": float(
            np.quantile(values, 0.10)
        ),
        "q90": float(
            np.quantile(values, 0.90)
        ),
        "std": float(
            np.std(values)
        ) if len(values) > 1 else 0.0
    }

    _REFERENCE_STATS_CACHE[cache_key] = stats

    return stats


def candidate_plausibility_penalty(
    patient,
    disease,
    changes
):
    """
    Lower is better.

    Penalize a candidate when it pushes changed features far outside
    the 1st-99th percentile of the reference training distribution.
    For categorical features this returns no distribution penalty.
    """

    disease = normalize_disease(
        disease
    )

    penalty = 0.0

    for feature, details in changes.items():

        new_value = details.get(
            "new"
        )

        if feature in CATEGORICAL_FEATURES.get(
            disease,
            set()
        ):
            continue

        stats = _reference_numeric_stats(
            disease,
            feature
        )

        if stats is None:
            continue

        numeric = safe_numeric(
            new_value
        )

        if not np.isfinite(
            numeric
        ):
            penalty += 5.0
            continue

        if numeric < stats["q01"]:
            width = max(
                stats["q90"] - stats["q10"],
                1e-9
            )
            penalty += (
                stats["q01"] - numeric
            ) / width

        elif numeric > stats["q99"]:
            width = max(
                stats["q90"] - stats["q10"],
                1e-9
            )
            penalty += (
                numeric - stats["q99"]
            ) / width

    return float(
        penalty
    )


def _candidate_direction_score(
    disease,
    original,
    new_value,
    feature,
    target_class
):
    """
    Soft preference only.

    This never overrides the trained model. It simply ranks
    scientifically interpretable directions higher when the feature
    has a well-known state direction in the project.

    1.0 = preferred direction
    0.5 = neutral / unknown
    0.0 = opposite of preferred direction

    target_class is the class the model must flip to.
    """

    disease = normalize_disease(
        disease
    )

    old = safe_numeric(
        original
    )
    new = safe_numeric(
        new_value
    )

    if not np.isfinite(old) or not np.isfinite(new):
        return 0.5

    delta = new - old

    if abs(delta) < 1e-12:
        return 0.5

    # ------------------------------------------------------------
    # DIABETES
    # Positive class should be associated with the presence of
    # symptom/state markers. Negative class is the reverse.
    # ------------------------------------------------------------

    diabetes_positive = {
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
    }

    if disease == "diabetes" and feature in diabetes_positive:
        if old in (0.0, 1.0) and new in (0.0, 1.0):
            expected_positive = new > old
            return (
                1.0
                if (
                    target_class == 1
                    and expected_positive
                ) or (
                    target_class == 0
                    and not expected_positive
                )
                else 0.0
            )

    # ------------------------------------------------------------
    # CKD
    # These are soft clinical-state directions used only for ranking.
    # ------------------------------------------------------------

    ckd_positive_up = {
        "al",
        "su",
        "rbc",
        "pc",
        "pcc",
        "ba",
        "bgr",
        "bu",
        "sc",
        "pot"
    }

    ckd_positive_down = {
        "sg",
        "hemo",
        "pcv"
    }

    ckd_positive_up_large = {
        "wbcc"
    }

    if disease == "ckd":

        if feature in ckd_positive_up:
            preferred_up = delta > 0

        elif feature in ckd_positive_down:
            preferred_up = delta < 0

        elif feature in ckd_positive_up_large:
            preferred_up = delta > 0

        else:
            preferred_up = None

        if preferred_up is not None:
            return (
                1.0
                if (
                    target_class == 1
                    and preferred_up
                ) or (
                    target_class == 0
                    and not preferred_up
                )
                else 0.0
            )

    # ------------------------------------------------------------
    # STROKE
    # ------------------------------------------------------------

    if disease == "stroke":

        if feature in {
            "hypertension",
        } and old in (0.0, 1.0) and new in (0.0, 1.0):

            positive_direction = new > old

            return (
                1.0
                if (
                    target_class == 1
                    and positive_direction
                ) or (
                    target_class == 0
                    and not positive_direction
                )
                else 0.0
            )

        if feature == "smoking_status":
            # Encoded values:
            # 0 never smoked
            # 1 formerly smoked
            # 2 smokes
            # 3 unknown
            if target_class == 1:
                return (
                    1.0 if new > old and new <= 2 else 0.5
                )
            if target_class == 0:
                return (
                    1.0 if new < old else 0.5
                )

        if feature in {
            "avg_glucose_level",
            "bmi"
        }:
            preferred_up = delta > 0

            return (
                0.75
                if (
                    target_class == 1
                    and preferred_up
                ) or (
                    target_class == 0
                    and not preferred_up
                )
                else 0.25
            )

    # ------------------------------------------------------------
    # HEART
    # ------------------------------------------------------------

    if disease == "heart":

        if feature in {
            "trestbps",
            "chol",
            "oldpeak"
        }:
            preferred_up = delta > 0

            return (
                0.85
                if (
                    target_class == 1
                    and preferred_up
                ) or (
                    target_class == 0
                    and not preferred_up
                )
                else 0.15
            )

        if feature == "thalach":
            preferred_up = delta < 0

            return (
                0.85
                if (
                    target_class == 1
                    and preferred_up
                ) or (
                    target_class == 0
                    and not preferred_up
                )
                else 0.15
            )

        if feature in {
            "fbs",
            "exang"
        } and old in (0.0, 1.0) and new in (0.0, 1.0):

            positive_direction = new > old

            return (
                0.85
                if (
                    target_class == 1
                    and positive_direction
                ) or (
                    target_class == 0
                    and not positive_direction
                )
                else 0.15
            )

    return 0.5


def _dedupe_numeric_values(
    values,
    current
):
    result = []

    for value in values:

        if not within_domain(
            "",
            value
        ):
            continue

        try:

            if current is not None and abs(
                float(value) - float(current)
            ) < 1e-12:
                continue

        except (
            TypeError,
            ValueError
        ):

            if str(value) == str(current):
                continue

        if all(
            (
                (
                    not np.isfinite(
                        safe_numeric(existing)
                    )
                )
                or
                (
                    not np.isfinite(
                        safe_numeric(value)
                    )
                )
                or
                abs(
                    safe_numeric(existing)
                    -
                    safe_numeric(value)
                ) >= 1e-12
            )
            for existing in result
        ):
            result.append(
                value
            )

    return result


# ============================================================
# CANDIDATE VALUES
# ============================================================

def candidate_values_for_feature(
    patient,
    disease,
    feature
):

    disease = normalize_disease(disease)
    original = patient.get(feature)

    if feature_is_immutable(disease, feature):
        return []

    values = get_reference_values(
        disease,
        feature,
        original
    )

    # --------------------------------------------------------
    # Explicit legal state spaces for categorical features.
    # --------------------------------------------------------
    categorical_spaces = {
        "heart": {
            "sex": [0, 1],
            "cp": [0, 1, 2, 3],
            "fbs": [0, 1],
            "restecg": [0, 1, 2],
            "exang": [0, 1],
            "slope": [0, 1, 2],
            "ca": [0, 1, 2, 3],
            "thal": [0, 1, 2]
        },
        "diabetes": {
            "gender": [0, 1],
            "polyuria": [0, 1],
            "polydipsia": [0, 1],
            "sudden_weight_loss": [0, 1],
            "weakness": [0, 1],
            "polyphagia": [0, 1],
            "genital_thrush": [0, 1],
            "visual_blurring": [0, 1],
            "itching": [0, 1],
            "irritability": [0, 1],
            "delayed_healing": [0, 1],
            "partial_paresis": [0, 1],
            "muscle_stiffness": [0, 1],
            "alopecia": [0, 1],
            "obesity": [0, 1]
        },
        "ckd": {
            "rbc": [0, 1],
            "pc": [0, 1],
            "pcc": [0, 1],
            "ba": [0, 1],
            "htn": [0, 1],
            "dm": [0, 1],
            "cad": [0, 1],
            "appet": [0, 1],
            "pe": [0, 1],
            "ane": [0, 1]
        },
        "stroke": {
            "gender": [0, 1, 2],
            "hypertension": [0, 1],
            "heart_disease": [0, 1],
            "ever_married": [0, 1],
            "work_type": [0, 1, 2, 3, 4],
            "Residence_type": [0, 1],
            "smoking_status": [0, 1, 2, 3]
        }
    }

    if feature in categorical_spaces.get(disease, {}):
        values = categorical_spaces[disease][feature]

    filtered = []
    for value in values:
        if not within_domain(feature, value):
            continue

        if feature in CATEGORICAL_FEATURES.get(disease, set()):
            numeric = safe_numeric(value)
            if not np.isfinite(numeric):
                continue

            allowed = categorical_spaces.get(disease, {}).get(feature)
            if allowed is not None and int(numeric) not in set(allowed):
                continue

        filtered.append(value)

    filtered = _dedupe_numeric_values(filtered, original)

    # --------------------------------------------------------
    # Numerical features: build a deliberately diverse search
    # set instead of only the nearest values.
    # --------------------------------------------------------
    if feature not in CATEGORICAL_FEATURES.get(disease, set()):
        current = safe_numeric(original)
        pool = list(filtered)
        stats = _reference_numeric_stats(disease, feature)

        if stats is not None:
            for key in ("q01", "q10", "median", "q90", "q99"):
                value = stats.get(key)
                if value is not None:
                    pool.append(float(value))

        bounds = DOMAIN_BOUNDS.get(feature)
        if bounds is not None:
            low, high = bounds
            pool.extend([float(low), float(high)])

        pool.extend(FALLBACK_VALUES.get(feature, []))

        if current is not None and np.isfinite(current):
            if stats is not None:
                if stats.get("q10") is not None:
                    pool.append(float(stats["q10"]))
                if stats.get("q90") is not None:
                    pool.append(float(stats["q90"]))

            # Moderate proportional anchors.
            pool.extend([
                current * 0.50,
                current * 0.75,
                current * 1.25,
                current * 1.50
            ])

        cleaned = []
        for value in pool:
            numeric = safe_numeric(value)
            if not np.isfinite(numeric):
                continue
            numeric = clean_value(numeric)
            if not within_domain(feature, numeric):
                continue
            if current is not None and np.isfinite(current):
                if abs(float(numeric) - current) < 1e-12:
                    continue
            if numeric not in cleaned:
                cleaned.append(numeric)

        if current is None or not np.isfinite(current):
            return sorted(cleaned)[:MAX_VALUES_PER_FEATURE]

        near = sorted(
            cleaned,
            key=lambda value: abs(float(value) - current)
        )
        far = sorted(
            cleaned,
            key=lambda value: abs(float(value) - current),
            reverse=True
        )
        lower = sorted(
            [value for value in cleaned if float(value) < current],
            key=lambda value: abs(float(value) - current)
        )
        upper = sorted(
            [value for value in cleaned if float(value) > current],
            key=lambda value: abs(float(value) - current)
        )

        selected = []

        def add(value):
            if value is None:
                return
            if any(values_equal(existing, value) for existing in selected):
                return
            selected.append(value)

        for value in near[:2]:
            add(value)
        for value in lower[:2]:
            add(value)
        for value in upper[:2]:
            add(value)
        for value in far[:2]:
            add(value)

        return sorted(
            selected,
            key=lambda value: abs(float(value) - current)
        )[:MAX_VALUES_PER_FEATURE]

    # Categorical: keep every alternate legal state, ordered by
    # closeness so sparse changes are still evaluated early.
    try:
        filtered = sorted(
            filtered,
            key=lambda value: abs(float(value) - float(original))
        )
    except (TypeError, ValueError):
        filtered = list(filtered)

    return filtered[:MAX_VALUES_PER_FEATURE]


# ============================================================
# BUILD CHANGE DETAILS
# ============================================================

def make_change_details(
    patient,
    feature,
    new_value,
    disease=None
):

    original = patient.get(
        feature
    )

    return {

        "old":
            clean_value(
                original
            ),

        "new":
            clean_value(
                new_value
            ),

        "normalized_change":
            round(
                calculate_change_magnitude(
                    original,
                    new_value,
                    disease=disease,
                    feature=feature
                ),
                6
            )
    }


def values_equal(
    old_value,
    new_value
):
    """
    Robust equality check for candidate generation/normalization.

    Handles:
    - numeric values with floating-point tolerance
    - strings/categories
    - None values
    """

    if old_value is None or new_value is None:
        return (
            old_value is None
            and
            new_value is None
        )

    try:

        old = float(
            old_value
        )

        new = float(
            new_value
        )

        if (
            np.isfinite(old)
            and
            np.isfinite(new)
        ):

            return abs(
                old - new
            ) < 1e-12

    except (
        TypeError,
        ValueError
    ):
        pass

    return (
        str(old_value).strip().lower()
        ==
        str(new_value).strip().lower()
    )

def generate_single_feature_candidates(
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

    ordered_features = sorted(
        feature_names,
        key=lambda feature: (
            feature_is_immutable(
                disease,
                feature
            ),
            feature_priority(
                disease,
                feature
            )
        )
    )

    candidates = []

    for feature in ordered_features:

        if feature_is_immutable(
            disease,
            feature
        ):
            continue

        values = candidate_values_for_feature(
            patient,
            disease,
            feature
        )

        for value in values:

            # Defensive guard: never create a fake "change".
            if values_equal(
                patient.get(feature),
                value
            ):
                continue

            candidates.append({
                feature:
                    make_change_details(
                        patient,
                        feature,
                        value,
                        disease=disease
                    )
            })

    return candidates


def generate_multi_feature_candidates(
    patient,
    disease,
    max_features_changed=2,
    max_candidates=MAX_TOTAL_CANDIDATES,
    target_class=None
):
    disease = normalize_disease(disease)
    feature_names = MODEL_CONFIG[disease]["features"]

    max_features_changed = max(
        1,
        min(int(max_features_changed), MAX_FEATURES_CHANGED)
    )

    if target_class is None:
        original_prediction, _ = predict_patient(patient, disease)
        target_class = 1 if int(original_prediction) == 0 else 0

    mutable_features = [
        feature for feature in feature_names
        if not feature_is_immutable(disease, feature)
    ]

    mutable_features = sorted(
        mutable_features,
        key=lambda feature: (
            feature_priority(disease, feature),
            feature
        )
    )

    feature_candidates = {}
    for feature in mutable_features:
        feature_candidates[feature] = candidate_values_for_feature(
            patient,
            disease,
            feature
        )[:MAX_VALUES_PER_FEATURE]

    candidate_buckets = []

    # --------------------------------------------------------
    # Build every allowed 2-feature combination. Each bucket is
    # scored before the global budget is applied so feature pairs
    # with a plausible class-changing direction are searched first.
    # --------------------------------------------------------
    for number_of_changes in range(2, max_features_changed + 1):
        for selected_features in itertools.combinations(
            mutable_features,
            number_of_changes
        ):
            value_lists = [
                feature_candidates.get(feature, [])
                for feature in selected_features
            ]

            if any(len(values) == 0 for values in value_lists):
                continue

            bucket = []
            for candidate_values in itertools.product(*value_lists):
                changes = {}
                valid = True

                for feature, new_value in zip(
                    selected_features,
                    candidate_values
                ):
                    original = patient.get(feature)

                    if values_equal(original, new_value):
                        valid = False
                        break

                    if not within_domain(feature, new_value):
                        valid = False
                        break

                    changes[feature] = make_change_details(
                        patient,
                        feature,
                        new_value,
                        disease=disease
                    )

                if not valid or len(changes) != number_of_changes:
                    continue

                direction_scores = [
                    _candidate_direction_score(
                        disease,
                        patient.get(feature),
                        details.get("new"),
                        feature,
                        target_class
                    )
                    for feature, details in changes.items()
                ]

                direction_score = (
                    float(np.mean(direction_scores))
                    if direction_scores
                    else 0.5
                )

                bucket.append({
                    "changes": changes,
                    "direction_score": direction_score,
                    "distance": candidate_distance(changes),
                    "plausibility": candidate_plausibility_penalty(
                        patient,
                        disease,
                        changes
                    )
                })

            if bucket:
                # Search promising directional changes before neutral
                # changes, then prefer smaller plausible movements.
                bucket.sort(
                    key=lambda item: (
                        -item["direction_score"],
                        item["plausibility"],
                        item["distance"]
                    )
                )

                pair_priority = sum(
                    feature_priority(disease, feature)
                    for feature in selected_features
                )

                bucket_score = max(
                    item["direction_score"]
                    for item in bucket
                )

                candidate_buckets.append({
                    "features": selected_features,
                    "priority": pair_priority,
                    "score": bucket_score,
                    "items": bucket
                })

    # Search the most plausible feature combinations first while
    # retaining round-robin coverage among similarly useful buckets.
    candidate_buckets.sort(
        key=lambda item: (
            -item["score"],
            item["priority"],
            len(item["features"])
        )
    )

    candidates = []
    bucket_index = 0

    while len(candidates) < max_candidates and candidate_buckets:
        active_buckets = 0

        for bucket in candidate_buckets:
            items = bucket["items"]

            if bucket_index < len(items):
                candidates.append(
                    items[bucket_index]["changes"]
                )
                active_buckets += 1

                if len(candidates) >= max_candidates:
                    break

        if active_buckets == 0:
            break

        bucket_index += 1

    return candidates

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

    disease = normalize_disease(
        disease
    )

    # Defensive cleanup:
    # Never evaluate a candidate containing unchanged features.
    cleaned_changes = {}

    for feature, details in changes.items():

        old_value = (
            details.get("old")
            if isinstance(details, dict)
            else patient.get(feature)
        )

        new_value = (
            details.get("new")
            if isinstance(details, dict)
            else details
        )

        if values_equal(
            patient.get(feature),
            new_value
        ):
            continue

        if feature_is_immutable(
            disease,
            feature
        ):
            return None

        cleaned_changes[
            feature
        ] = make_change_details(
            patient,
            feature,
            new_value,
            disease=disease
        )

    if not cleaned_changes:
        return None

    candidate_patient = apply_changes(
        patient,
        {
            feature:
                details["new"]
            for feature, details
            in cleaned_changes.items()
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

        print(
            "Counterfactual candidate error:",
            repr(error)
        )

        return None

    probability = float(
        probability
    )

    # ------------------------------------------------------------
    # Determine the actual production boundary.
    # ------------------------------------------------------------
    threshold = get_decision_threshold(
        disease
    )

    expected_candidate_prediction = int(
        probability >= threshold
    )

    # The probability and class MUST agree.
    if (
        int(prediction)
        !=
        expected_candidate_prediction
    ):
        return None

    # ------------------------------------------------------------
    # Must actually cross the model decision boundary.
    # ------------------------------------------------------------
    if int(prediction) == int(
        original_prediction
    ):
        return None

    number_of_changes = len(
        cleaned_changes
    )

    normalized_change = candidate_distance(
        cleaned_changes
    )

    plausibility_penalty = (
        candidate_plausibility_penalty(
            patient,
            disease,
            cleaned_changes
        )
    )

    target_class = int(
        prediction
    )

    direction_scores = [
        _candidate_direction_score(
            disease,
            patient.get(feature),
            details.get("new"),
            feature,
            target_class
        )
        for feature, details
        in cleaned_changes.items()
    ]

    direction_score = (
        float(
            np.mean(
                direction_scores
            )
        )
        if direction_scores
        else 0.5
    )

    return {
        "changes":
            cleaned_changes,

        "prediction":
            target_class,

        "prediction_class":
            target_class,

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
            ),

        "_disease":
            disease,

        "_boundary_margin":
            round(
                candidate_boundary_margin(
                    probability,
                    disease
                ),
                8
            ),

        "_plausibility_penalty":
            round(
                plausibility_penalty,
                6
            ),

        "_direction_score":
            round(
                direction_score,
                6
            ),

        "_feature_priority":
            min(
                feature_priority(
                    disease,
                    feature
                )
                for feature in cleaned_changes
            )
            if cleaned_changes
            else 999
    }


def get_decision_threshold(
    disease
):
    disease = normalize_disease(
        disease
    )

    # Heart / Diabetes / CKD production models use model.predict().
    # Their model decision threshold is therefore owned by the model.
    # Stroke explicitly uses stroke_threshold.
    if disease == "stroke":
        return float(
            stroke_threshold
        )

    return 0.5


def candidate_boundary_margin(
    probability,
    disease
):
    """
    Distance of a candidate probability from the decision boundary.

    Smaller is better once the class has flipped: the counterfactual
    lies closer to the model's actual decision boundary rather than
    simply being an extreme point in the target class.
    """

    try:
        return abs(
            float(probability)
            -
            get_decision_threshold(
                disease
            )
        )
    except (
        TypeError,
        ValueError
    ):
        return 999999.0

def _candidate_quality_key(
    item
):

    disease = item.get(
        "_disease",
        "heart"
    )

    return (
        # 1. Fewer real feature changes.
        item.get(
            "number_of_changes",
            999
        ),

        # 2. Stay inside observed/reference distributions.
        item.get(
            "_plausibility_penalty",
            999999
        ),

        # 3. Prefer candidates close to the actual
        #    decision boundary after crossing it.
        item.get(
            "_boundary_margin",
            candidate_boundary_margin(
                item.get(
                    "probability",
                    0
                ),
                disease
            )
        ),

        # 4. Prefer interpretable direction.
        -item.get(
            "_direction_score",
            0.5
        ),

        # 5. Prefer smaller normalized movement.
        item.get(
            "normalized_change",
            999999
        ),

        # 6. Stable feature-priority tie breaker.
        item.get(
            "_feature_priority",
            999
        )
    )


def sort_counterfactuals(
    counterfactuals
):

    return sorted(
        counterfactuals,
        key=_candidate_quality_key
    )

def select_diverse_counterfactuals(
    counterfactuals,
    max_results
):
    if not counterfactuals:
        return []

    ranked = sort_counterfactuals(
        counterfactuals
    )

    selected = []

    used_feature_sets = set()
    used_features = set()

    # --------------------------------------------------------
    # PASS 1
    # Prefer unique combinations of changed features.
    # Example:
    #   {ca, oldpeak}
    #   {ca, restecg}
    #   {trestbps, thalach}
    # are treated as different explanation patterns.
    # --------------------------------------------------------
    for item in ranked:

        if len(selected) >= max_results:
            break

        changes = item.get(
            "changes",
            {}
        )

        if not changes:
            continue

        feature_set = frozenset(
            changes.keys()
        )

        if feature_set in used_feature_sets:
            continue

        selected.append(
            item
        )

        used_feature_sets.add(
            feature_set
        )

        used_features.update(
            feature_set
        )

    # --------------------------------------------------------
    # PASS 2
    # Prefer a new individual feature when possible.
    # This prevents five results from revolving around the
    # exact same dominant feature.
    # --------------------------------------------------------
    if len(selected) < max_results:

        for item in ranked:

            if len(selected) >= max_results:
                break

            if item in selected:
                continue

            changes = item.get(
                "changes",
                {}
            )

            feature_set = frozenset(
                changes.keys()
            )

            # Unique combination still preferred.
            if feature_set in used_feature_sets:
                continue

            # Prefer at least one new feature.
            if not feature_set.isdisjoint(
                used_features
            ):
                continue

            selected.append(
                item
            )

            used_feature_sets.add(
                feature_set
            )

            used_features.update(
                feature_set
            )

    # --------------------------------------------------------
    # PASS 3
    # Fill remaining slots with the best valid candidates.
    # At this point all remaining items are already genuine
    # model-validated counterfactuals.
    # --------------------------------------------------------
    if len(selected) < max_results:

        for item in ranked:

            if len(selected) >= max_results:
                break

            if item in selected:
                continue

            selected.append(
                item
            )

    return selected[
        :max_results
    ]

# ============================================================
# FIND COUNTERFACTUALS
# ============================================================

def find_counterfactuals(
    patient,
    disease="heart",
    max_results=5,
    max_features_changed=2
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
    # Search in two stages:
    #
    # 1) Single-feature counterfactuals first. These are the
    #    sparsest and easiest to interpret.
    #
    # 2) Multi-feature combinations only when needed to obtain
    #    enough valid/diverse counterfactuals.
    # --------------------------------------------------------

    single_candidates = (
        generate_single_feature_candidates(
            patient_dict,
            disease
        )
    )

    multi_candidates = []

    # We only need a bounded number of multi-feature candidates
    # after single-feature candidates have been examined.
    if max_features_changed > 1:
        multi_candidates = (
            generate_multi_feature_candidates(
                patient_dict,
                disease,
                max_features_changed=max_features_changed,
                max_candidates=MAX_TOTAL_CANDIDATES,
                target_class=(1 if original_prediction == 0 else 0)
            )
        )

    candidates = (
        single_candidates +
        multi_candidates
    )

    print(
        "Single-feature candidates:",
        len(single_candidates)
    )

    print(
        "Multi-feature candidates:",
        len(multi_candidates)
    )

    print(
        "Total candidates:",
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

        # Once we have many valid candidates, the final
        # diversity selector will choose the best five.
        if len(found) >= max(
            max_results * 20,
            50
        ):
            break

    print(
        "Candidates Tested:",
        total_tested
    )

    print(
        "Valid Counterfactuals:",
        len(found)
    )

    # --------------------------------------------------------
    # Select sparse, plausible and diverse counterfactuals.
    # --------------------------------------------------------

    found = select_diverse_counterfactuals(
        found,
        max_results
    )

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
            "Stroke"
            if prediction == 1
            else
            "No Stroke"
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

    def display_value(
        feature,
        value
    ):
        # --------------------------------------------------------
        # Stroke category decoding for clinician-facing output.
        # The model may internally use numeric category codes, but
        # the API/UI should expose the original category labels.
        # --------------------------------------------------------
        if disease == "stroke":

            try:
                code = int(
                    float(value)
                )
            except (
                TypeError,
                ValueError
            ):
                return value

            mappings = {
                "gender":
                    STROKE_GENDER_VALUES,

                "ever_married":
                    STROKE_MARRIED_VALUES,

                "work_type":
                    STROKE_WORK_VALUES,

                "Residence_type":
                    STROKE_RESIDENCE_VALUES,

                "smoking_status":
                    STROKE_SMOKING_VALUES
            }

            mapping = mappings.get(
                feature
            )

            if mapping is not None:
                return mapping.get(
                    code,
                    value
                )

        # --------------------------------------------------------
        # Diabetes frontend representation.
        # --------------------------------------------------------
        if disease == "diabetes":

            if feature == "gender":

                try:
                    return (
                        "Male"
                        if int(float(value)) == 1
                        else "Female"
                    )
                except (
                    TypeError,
                    ValueError
                ):
                    return value

            if feature in {
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
            }:

                try:
                    return (
                        "Yes"
                        if int(float(value)) == 1
                        else "No"
                    )
                except (
                    TypeError,
                    ValueError
                ):
                    return value

        # --------------------------------------------------------
        # CKD frontend representation.
        # --------------------------------------------------------
        if disease == "ckd":

            if feature == "appet":

                try:
                    return (
                        "Poor"
                        if int(float(value)) == 1
                        else "Good"
                    )
                except (
                    TypeError,
                    ValueError
                ):
                    return value

            if feature in {
                "rbc",
                "pc",
                "pcc",
                "ba",
                "htn",
                "dm",
                "cad",
                "pe",
                "ane"
            }:

                try:
                    return (
                        "Yes"
                        if int(float(value)) == 1
                        else "No"
                    )
                except (
                    TypeError,
                    ValueError
                ):
                    return value

        return clean_value(
            value
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

            continue

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

                if feature_is_immutable(
                    disease,
                    feature
                ):
                    continue

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

                elif isinstance(
                    value,
                    (list, tuple)
                ):

                    if len(value) >= 2:
                        old_value = value[0]
                        new_value = value[1]
                    elif len(value) == 1:
                        old_value = None
                        new_value = value[0]
                    else:
                        old_value = None
                        new_value = None

                else:

                    old_value = None
                    new_value = value

                # Never expose an unchanged feature as a change.
                if (
                    old_value is not None
                    and
                    values_equal(
                        old_value,
                        new_value
                    )
                ):
                    continue

                normalized_changes[
                    feature
                ] = {
                    "old":
                        display_value(
                            feature,
                            old_value
                        ),

                    "new":
                        display_value(
                            feature,
                            new_value
                        )
                }

        # The number of changes is always recalculated from the
        # final cleaned change dictionary. Never trust a stale value
        # supplied by a caller or older backend version.
        number_of_changes = len(
            normalized_changes
        )

        if number_of_changes == 0:
            continue

        probability = cf.get(
            "probability",
            cf.get(
                "new_probability",
                0
            )
        )

        try:

            probability = float(
                probability
            )

            if not (
                0.0 <= probability <= 1.0
            ):
                continue

        except (
            TypeError,
            ValueError
        ):

            continue

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

            if not np.isfinite(
                normalized_change
            ):
                normalized_change = 0.0

        except (
            TypeError,
            ValueError
        ):

            normalized_change = 0.0

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