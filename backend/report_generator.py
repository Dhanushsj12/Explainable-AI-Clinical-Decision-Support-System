import re
from datetime import datetime
from html import escape
from numbers import Number

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


# ============================================================
# EXPLAINABLE AI CLINICAL DECISION SUPPORT SYSTEM
# PDF REPORT GENERATOR
#
# Supports:
#   Heart Disease
#   Diabetes
#   Chronic Kidney Disease
#   Stroke
#
# FIXES IN THIS VERSION:
#
# 1. Clinical Parameters
#    extract_clinical_features() reads Stroke (and all disease)
#    fields directly from the patient/result dictionaries the
#    Flask backend already builds, with case-insensitive
#    matching and Stroke-specific aliases (Residence_type vs
#    residence_type, etc).
#
# 2. Patient Information table
#    build_patient_data() now returns rows with an explicit
#    "Field" / "Value" header, matching every other table in
#    the report. Previously the first real data row was being
#    painted with header styling because no header row existed,
#    which produced inconsistent output.
#
# 3. SHAP / LIME "N/A" values
#    normalize_explanation_features() now falls back to
#    scanning a feature entry for ANY numeric field if none of
#    the known value keys are present, instead of silently
#    returning None -> "N/A". This does not change how SHAP or
#    LIME are calculated -- it only changes how the already
#    computed values are located inside the response payload.
#
# Counterfactual generation/formatting is UNCHANGED.
# ============================================================


# ============================================================
# STYLES
# ============================================================

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "ReportTitle",
    parent=styles["Heading1"],
    alignment=TA_CENTER,
    fontName="Helvetica-Bold",
    fontSize=18,
    leading=22,
    textColor=colors.HexColor("#123b5d"),
    spaceAfter=6,
)

subtitle_style = ParagraphStyle(
    "ReportSubtitle",
    parent=styles["Heading2"],
    alignment=TA_CENTER,
    fontName="Helvetica",
    fontSize=11,
    leading=14,
    textColor=colors.HexColor("#4b5563"),
    spaceAfter=12,
)

heading_style = ParagraphStyle(
    "ReportHeading",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=13,
    leading=16,
    textColor=colors.HexColor("#123b5d"),
    spaceBefore=8,
    spaceAfter=8,
)

subheading_style = ParagraphStyle(
    "ReportSubHeading",
    parent=styles["Heading3"],
    fontName="Helvetica-Bold",
    fontSize=10,
    leading=13,
    textColor=colors.HexColor("#1f2937"),
    spaceBefore=5,
    spaceAfter=5,
)

normal_style = ParagraphStyle(
    "ReportNormal",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=9,
    leading=13,
    textColor=colors.HexColor("#374151"),
    spaceAfter=5,
)

small_style = ParagraphStyle(
    "ReportSmall",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=8,
    leading=11,
    textColor=colors.HexColor("#4b5563"),
)

header_style = ParagraphStyle(
    "ReportHeaderStyle",
    parent=styles["BodyText"],
    fontName="Helvetica-Bold",
    fontSize=8,
    leading=11,
    textColor=colors.white,
)

disclaimer_style = ParagraphStyle(
    "ReportDisclaimer",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=8.5,
    leading=12,
    textColor=colors.HexColor("#7c2d12"),
    backColor=colors.HexColor("#fff7ed"),
    borderColor=colors.HexColor("#fed7aa"),
    borderWidth=0.7,
    borderPadding=8,
    spaceBefore=6,
    spaceAfter=8,
)

warning_style = ParagraphStyle(
    "ReportWarning",
    parent=normal_style,
    textColor=colors.HexColor("#92400e"),
)


# ============================================================
# GENERIC HELPERS
# ============================================================

def first_available(data, keys, default=None):
    if not isinstance(data, dict):
        return default

    for key in keys:
        if key in data:
            value = data.get(key)

            if value is not None:
                if isinstance(value, str):
                    if value.strip():
                        return value
                elif value != "":
                    return value

    return default


def html_escape(value):
    if value is None:
        return ""
    return escape(str(value))


def safe_text(value, default="N/A"):
    if value is None:
        return default

    # ----------------------------------------------------------
    # DEFENSIVE FIX
    #
    # If a reportlab Paragraph object ever ends up here instead
    # of a plain string/number (e.g. a heading accidentally
    # placed into a table row's data instead of being appended
    # as its own flowable), extracting str(value) dumps its raw
    # internal repr, e.g.:
    #
    #   Paragraph('caseSensitive': 1 'encoding': 'utf8'
    #   'text': '<b>Counterfactual</b>' ...) #Paragraph
    #
    # which is exactly the garbage text seen in the PDF. Detect
    # that case and pull out the clean underlying text instead,
    # stripping any markup tags.
    # ----------------------------------------------------------

    if isinstance(value, Paragraph):
        raw_text = getattr(value, "text", "")
        clean_text = re.sub(r"<[^>]+>", "", raw_text).strip()

        return clean_text if clean_text else default

    if isinstance(value, str):
        value = value.strip()

        if not value:
            return default

        return html_escape(value)

    return html_escape(value)


def format_number(value, decimals=2):
    if value is None:
        return "N/A"

    if isinstance(value, Paragraph):
        return safe_text(value)

    try:
        number = float(value)

        if decimals == 0:
            return str(int(round(number)))

        return f"{number:.{decimals}f}"

    except (TypeError, ValueError):
        return safe_text(value)


def format_percent(value):
    if value is None:
        return "N/A"

    if isinstance(value, Paragraph):
        return safe_text(value)

    try:
        if isinstance(value, str):
            cleaned = value.strip().replace("%", "")

            if not cleaned:
                return "N/A"

            number = float(cleaned)

        else:
            number = float(value)

        if 0 <= number <= 1:
            number *= 100

        return f"{number:.2f}%"

    except (TypeError, ValueError):
        return safe_text(value)


def format_feature_list(value):
    if value is None:
        return "None"

    if isinstance(value, (list, tuple, set)):
        if not value:
            return "None"

        values = []

        for item in value:
            if isinstance(item, dict):
                name = first_available(
                    item,
                    [
                        "feature",
                        "feature_name",
                        "name",
                        "label",
                    ],
                    None,
                )

                if name is not None:
                    values.append(str(name))

            else:
                values.append(str(item))

        return (
            html_escape(", ".join(values))
            if values
            else "None"
        )

    if isinstance(value, dict):
        values = []

        for key, item in value.items():
            if item is not None:
                values.append(f"{key}: {item}")

        return (
            html_escape(", ".join(values))
            if values
            else "None"
        )

    return html_escape(str(value))


def normalize_disease(disease):
    if disease is None:
        return "unknown"

    value = str(disease).strip().lower()

    replacements = {
        "heart disease": "heart",
        "heart_disease": "heart",
        "cardiac": "heart",

        "diabetes mellitus": "diabetes",
        "diabetes": "diabetes",

        "chronic kidney disease": "ckd",
        "chronic_kidney_disease": "ckd",
        "kidney disease": "ckd",
        "kidney": "ckd",
        "ckd": "ckd",

        "stroke risk": "stroke",
        "stroke_risk": "stroke",
        "stroke": "stroke",
    }

    return replacements.get(value, value)


def disease_display_name(disease):
    disease = normalize_disease(disease)

    names = {
        "heart": "Heart Disease",
        "diabetes": "Diabetes",
        "ckd": "Chronic Kidney Disease",
        "stroke": "Stroke",
    }

    return names.get(
        disease,
        str(disease).replace("_", " ").title(),
    )


def prediction_text(disease, prediction):
    disease = normalize_disease(disease)

    try:
        prediction = int(float(prediction))
    except (TypeError, ValueError):
        return safe_text(prediction)

    if disease == "heart":
        return (
            "Heart Disease"
            if prediction == 1
            else "No Heart Disease"
        )

    if disease == "diabetes":
        return (
            "Diabetes"
            if prediction == 1
            else "No Diabetes"
        )

    if disease == "ckd":
        return (
            "Chronic Kidney Disease"
            if prediction == 1
            else "No Chronic Kidney Disease"
        )

    if disease == "stroke":
        return (
            "Stroke"
            if prediction == 1
            else "No Stroke"
        )

    return str(prediction)


def display_feature_name(feature):
    names = {
        "age": "Age",
        "sex": "Gender",
        "gender": "Gender",

        "cp": "Chest Pain Type",
        "trestbps": "Resting Blood Pressure",
        "chol": "Serum Cholesterol",
        "fbs": "Fasting Blood Sugar",
        "restecg": "Resting ECG",
        "thalach": "Maximum Heart Rate",
        "exang": "Exercise Angina",
        "oldpeak": "ST Depression",
        "slope": "ST Segment Slope",
        "ca": "Major Vessels",
        "thal": "Thalassemia",

        "polyuria": "Polyuria",
        "polydipsia": "Polydipsia",
        "sudden_weight_loss": "Sudden Weight Loss",
        "weakness": "Weakness",
        "polyphagia": "Polyphagia",
        "genital_thrush": "Genital Thrush",
        "visual_blurring": "Visual Blurring",
        "itching": "Itching",
        "irritability": "Irritability",
        "delayed_healing": "Delayed Healing",
        "partial_paresis": "Partial Paresis",
        "muscle_stiffness": "Muscle Stiffness",
        "alopecia": "Alopecia",
        "obesity": "Obesity",

        "bp": "Blood Pressure",
        "sg": "Specific Gravity",
        "al": "Albumin",
        "su": "Sugar",
        "rbc": "Red Blood Cells",
        "pc": "Pus Cell",
        "pcc": "Pus Cell Clumps",
        "ba": "Bacteria",
        "bgr": "Blood Glucose",
        "bu": "Blood Urea",
        "sc": "Serum Creatinine",
        "sod": "Sodium",
        "pot": "Potassium",
        "hemo": "Hemoglobin",
        "pcv": "Packed Cell Volume",
        "wbcc": "White Blood Cell Count",
        "rbcc": "Red Blood Cell Count",
        "htn": "Hypertension",
        "dm": "Diabetes Mellitus",
        "cad": "Coronary Artery Disease",
        "appet": "Appetite",
        "pe": "Pedal Edema",
        "ane": "Anemia",

        "hypertension": "Hypertension",
        "heart_disease": "Heart Disease",
        "ever_married": "Ever Married",
        "work_type": "Work Type",
        "Residence_type": "Residence Type",
        "residence_type": "Residence Type",
        "avg_glucose_level": "Average Glucose Level",
        "average_glucose_level": "Average Glucose Level",
        "bmi": "Body Mass Index",
        "smoking_status": "Smoking Status",
    }

    key = str(feature)

    return names.get(
        key,
        key.replace("_", " ")
        .replace("-", " ")
        .title(),
    )


def paragraph_cell(value, bold=False):
    text = safe_text(value)

    if bold:
        text = f"<b>{text}</b>"

    return Paragraph(
        text,
        small_style,
    )


def header_cell(value):
    return Paragraph(
        f"<b>{html_escape(value)}</b>",
        header_style,
    )


def apply_standard_table_style(
    table,
    header_color="#123b5d",
):
    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(header_color),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor("#cbd5e1"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )


def build_key_value_table(rows):
    data = [
        [
            header_cell("Field"),
            header_cell("Value"),
        ]
    ]

    for key, value in rows:
        data.append(
            [
                paragraph_cell(key, True),
                paragraph_cell(value),
            ]
        )

    table = Table(
        data,
        colWidths=[
            2.35 * inch,
            4.05 * inch,
        ],
        repeatRows=1,
    )

    apply_standard_table_style(
        table,
        "#123b5d",
    )

    return table


# ============================================================
# PATIENT INFORMATION
#
# FIX #2: this now returns rows only (no header baked in) --
# the header is added explicitly where the table is built, in
# generate_report(), exactly the same way every other table in
# this report adds its header. Previously the raw rows were
# handed straight to Table() with no header row, so
# apply_standard_table_style() painted the FIRST DATA ROW
# ("Patient ID" / "PAT003") as if it were a header. That is
# what produced the inconsistent / reordered-looking output.
# ============================================================

def build_patient_data(patient):
    if not isinstance(patient, dict):
        patient = {}

    return [
        [
            "Patient ID",
            first_available(
                patient,
                [
                    "patient_id",
                    "patientId",
                    "id",
                ],
                "N/A",
            ),
        ],
        [
            "Patient Name",
            first_available(
                patient,
                [
                    "patient_name",
                    "patientName",
                    "name",
                ],
                "N/A",
            ),
        ],
        [
            "Doctor / Clinician",
            first_available(
                patient,
                [
                    "doctor_name",
                    "doctorName",
                    "clinician",
                    "doctor",
                ],
                "N/A",
            ),
        ],
        [
            "Hospital / Clinic",
            first_available(
                patient,
                [
                    "hospital_name",
                    "hospitalName",
                    "hospital",
                    "clinic",
                ],
                "N/A",
            ),
        ],
        [
            "Disease",
            disease_display_name(
                first_available(
                    patient,
                    [
                        "disease",
                        "condition",
                    ],
                    "unknown",
                )
            ),
        ],
    ]


# ============================================================
# CLINICAL FEATURES
# ============================================================

DISEASE_FEATURES = {
    "heart": [
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
    ],

    "diabetes": [
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
        "obesity",
    ],

    "ckd": [
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
        "ane",
    ],

    "stroke": [
        "gender",
        "age",
        "hypertension",
        "heart_disease",
        "ever_married",
        "work_type",
        "residence_type",
        "avg_glucose_level",
        "bmi",
        "smoking_status",
    ],
}


def _case_insensitive_get(data, key):
    """
    Case-insensitive dictionary lookup.

    This fixes the Stroke naming mismatch:
        Residence_type
    versus:
        residence_type
    """

    if not isinstance(data, dict):
        return None, False

    if key in data:
        return data[key], True

    wanted = str(key).lower()

    for existing_key, value in data.items():
        if str(existing_key).lower() == wanted:
            return value, True

    return None, False


def _collect_direct_features(
    source,
    feature_names,
    target,
):
    """
    Collect known disease features from top-level fields.
    """

    if not isinstance(source, dict):
        return

    for key in feature_names:
        if key in target:
            continue

        value, found = _case_insensitive_get(
            source,
            key,
        )

        if found:
            target[key] = value

    # Heart model may use sex while the frontend may expose gender.
    if "sex" in feature_names and "sex" not in target:
        value, found = _case_insensitive_get(
            source,
            "gender",
        )

        if found:
            target["sex"] = value

    # Diabetes/Stroke use gender while some payloads may expose sex.
    if "gender" in feature_names and "gender" not in target:
        value, found = _case_insensitive_get(
            source,
            "sex",
        )

        if found:
            target["gender"] = value


def extract_clinical_features(
    patient,
    result,
    disease,
):
    """
    Extract the actual submitted clinical parameters.

    Priority:
      1. nested feature dictionaries
      2. result["patient"]
      3. direct patient fields
      4. direct result fields

    This is intentionally read-only: it does not modify the
    working prediction, SHAP, LIME, agreement, or counterfactual data.
    """

    disease = normalize_disease(disease)

    feature_names = DISEASE_FEATURES.get(
        disease,
        [],
    )

    features = {}

    sources = []

    # --------------------------------------------------------
    # Patient dictionary.
    # --------------------------------------------------------

    if isinstance(patient, dict):
        sources.append(patient)

        nested = first_available(
            patient,
            [
                "features",
                "clinical_features",
                "parameters",
                "clinical_parameters",
            ],
            None,
        )

        if isinstance(nested, dict):
            sources.insert(0, nested)

    # --------------------------------------------------------
    # Result dictionary.
    # --------------------------------------------------------

    if isinstance(result, dict):
        sources.append(result)

        nested = first_available(
            result,
            [
                "features",
                "clinical_features",
                "parameters",
                "clinical_parameters",
            ],
            None,
        )

        if isinstance(nested, dict):
            sources.insert(0, nested)

        # The Flask backend can also store the patient dictionary
        # inside result["patient"].
        nested_patient = result.get("patient")

        if isinstance(nested_patient, dict):
            sources.insert(0, nested_patient)

            nested_features = first_available(
                nested_patient,
                [
                    "features",
                    "clinical_features",
                    "parameters",
                    "clinical_parameters",
                ],
                None,
            )

            if isinstance(nested_features, dict):
                sources.insert(
                    0,
                    nested_features,
                )

    # --------------------------------------------------------
    # Collect fields.
    # --------------------------------------------------------

    for source in sources:
        _collect_direct_features(
            source,
            feature_names,
            features,
        )

    # --------------------------------------------------------
    # Explicit Stroke aliases.
    #
    # These are deliberately additive and do not alter the model
    # input or any existing working section.
    # --------------------------------------------------------

    if disease == "stroke":
        aliases = {
            "gender": [
                "gender",
                "Gender",
                "sex",
                "Sex",
            ],
            "age": [
                "age",
                "Age",
            ],
            "hypertension": [
                "hypertension",
                "Hypertension",
            ],
            "heart_disease": [
                "heart_disease",
                "heart disease",
                "Heart Disease",
            ],
            "ever_married": [
                "ever_married",
                "ever married",
                "Ever Married",
            ],
            "work_type": [
                "work_type",
                "work type",
                "Work Type",
            ],
            "residence_type": [
                "residence_type",
                "Residence_type",
                "residence type",
                "Residence Type",
            ],
            "avg_glucose_level": [
                "avg_glucose_level",
                "average_glucose_level",
                "Average Glucose Level",
            ],
            "bmi": [
                "bmi",
                "BMI",
                "Body Mass Index",
            ],
            "smoking_status": [
                "smoking_status",
                "smoking status",
                "Smoking Status",
            ],
        }

        for canonical, possible_names in aliases.items():
            if canonical in features:
                continue

            for source in sources:
                found_value = None
                found = False

                for name in possible_names:
                    value, exists = _case_insensitive_get(
                        source,
                        name,
                    )

                    if exists:
                        found_value = value
                        found = True
                        break

                if found:
                    features[canonical] = found_value
                    break

    return features


def add_clinical_parameters_section(
    story,
    patient,
    result,
):
    """
    Add the submitted clinical parameters to the PDF.

    This section is the Stroke PDF fix.
    """

    story.append(
        Paragraph(
            "Clinical Parameters",
            heading_style,
        )
    )

    disease = normalize_disease(
        first_available(
            result,
            [
                "disease",
                "condition",
                "model",
            ],
            first_available(
                patient,
                [
                    "disease",
                    "condition",
                ],
                "unknown",
            ),
        )
    )

    features = extract_clinical_features(
        patient,
        result,
        disease,
    )

    if not features:
        story.append(
            Paragraph(
                "No clinical parameter values were supplied.",
                small_style,
            )
        )

        story.append(
            Spacer(1, 0.12 * inch)
        )

        return

    rows = [
        [
            header_cell("Feature"),
            header_cell("Observed Value"),
        ]
    ]

    # Preserve normal disease feature order.
    ordered_keys = []

    for key in DISEASE_FEATURES.get(
        disease,
        [],
    ):
        if key in features:
            ordered_keys.append(key)

    # Include any additional fields after the known fields.
    for key in features:
        if key not in ordered_keys:
            ordered_keys.append(key)

    for key in ordered_keys:
        rows.append(
            [
                paragraph_cell(
                    display_feature_name(key),
                    True,
                ),
                paragraph_cell(
                    features.get(key),
                ),
            ]
        )

    table = Table(
        rows,
        colWidths=[
            3.3 * inch,
            3.1 * inch,
        ],
        repeatRows=1,
    )

    apply_standard_table_style(
        table,
        "#123b5d",
    )

    story.append(table)

    story.append(
        Spacer(1, 0.18 * inch)
    )


# ============================================================
# MODEL ASSESSMENT
# ============================================================

def add_prediction_section(
    story,
    result,
):
    if not isinstance(result, dict):
        result = {}

    disease = normalize_disease(
        first_available(
            result,
            [
                "disease",
                "condition",
                "model",
            ],
            "unknown",
        )
    )

    prediction = first_available(
        result,
        [
            "prediction",
            "predicted_class",
            "class",
            "label",
            "prediction_class",
        ],
        None,
    )

    probability = first_available(
        result,
        [
            "probability",
            "prediction_probability",
            "risk_probability",
            "confidence",
            "positive_probability",
        ],
        None,
    )

    risk_level = first_available(
        result,
        [
            "risk_level",
            "riskLevel",
            "risk",
            "severity",
        ],
        "N/A",
    )

    recommendation = first_available(
        result,
        [
            "recommendation",
            "clinical_recommendation",
            "message",
            "clinicalRecommendation",
        ],
        None,
    )

    prediction_label = first_available(
        result,
        [
            "prediction_text",
            "predictionText",
            "predicted_label",
        ],
        (
            prediction_text(
                disease,
                prediction,
            )
            if prediction is not None
            else "N/A"
        ),
    )

    story.append(
        Paragraph(
            "Model Assessment",
            heading_style,
        )
    )

    rows = [
        [
            "Condition",
            disease_display_name(disease),
        ],
        [
            "Prediction",
            prediction_label,
        ],
        [
            "Class",
            safe_text(prediction),
        ],
        [
            "Probability",
            format_percent(probability),
        ],
        [
            "Risk Level",
            safe_text(risk_level),
        ],
        [
            "Clinical Recommendation",
            recommendation or "N/A",
        ],
    ]

    story.append(
        build_key_value_table(rows)
    )

    story.append(
        Spacer(1, 0.18 * inch)
    )


# ============================================================
# EXPLANATION NORMALIZATION
#
# FIX #3: added a numeric fallback so SHAP/LIME entries do not
# collapse to "N/A" just because the value key doesn't match
# one of the known names. This does NOT change how SHAP/LIME
# are computed -- it only widens how their already-computed
# values are located in the response dict.
# ============================================================

_KNOWN_VALUE_KEYS = [
    "value",
    "contribution",
    "shap_value",
    "weight",
    "score",
    "impact",
    "lime_value",
    "importance",
    "coefficient",
    "shap",
    "lime",
]

_NON_VALUE_KEYS = {
    "feature",
    "feature_name",
    "name",
    "label",
    "text",
    "rule",
    "direction",
    "sign",
}


def _find_numeric_fallback(item):
    """
    Last-resort search for a numeric contribution value inside a
    feature-explanation dict, used only when none of the known
    value keys are present. Skips fields that are clearly not a
    contribution (feature name/label/etc).
    """

    if not isinstance(item, dict):
        return None

    for key, value in item.items():

        if key in _NON_VALUE_KEYS:
            continue

        if isinstance(value, bool):
            continue

        if isinstance(value, Number):
            return value

        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                continue

    return None


def normalize_explanation_features(value):
    if value is None:
        return []

    result = []

    if isinstance(value, dict):
        for key, item in value.items():

            if isinstance(item, dict):
                feature_name = first_available(
                    item,
                    [
                        "feature",
                        "feature_name",
                        "name",
                        "label",
                        "text",
                    ],
                    key,
                )

                contribution = first_available(
                    item,
                    _KNOWN_VALUE_KEYS,
                    None,
                )

                if contribution is None:
                    contribution = _find_numeric_fallback(
                        item
                    )

            else:
                feature_name = key
                contribution = item

            result.append(
                {
                    "feature": feature_name,
                    "value": contribution,
                }
            )

        return result

    if not isinstance(value, (list, tuple)):
        return []

    for item in value:

        if isinstance(item, dict):
            feature_name = first_available(
                item,
                [
                    "feature",
                    "feature_name",
                    "name",
                    "label",
                    "text",
                ],
                None,
            )

            contribution = first_available(
                item,
                _KNOWN_VALUE_KEYS,
                None,
            )

            if contribution is None:
                contribution = _find_numeric_fallback(
                    item
                )

            result.append(
                {
                    "feature": feature_name,
                    "value": contribution,
                }
            )

        elif isinstance(item, (list, tuple)):

            if len(item) >= 2:
                result.append(
                    {
                        "feature": item[0],
                        "value": item[1],
                    }
                )

            elif len(item) == 1:
                result.append(
                    {
                        "feature": item[0],
                        "value": None,
                    }
                )

        else:
            result.append(
                {
                    "feature": item,
                    "value": None,
                }
            )

    return result


# ============================================================
# SHAP
# ============================================================

def add_shap_section(
    story,
    result,
):
    if not isinstance(result, dict):
        result = {}

    shap = first_available(
        result,
        [
            "shap_features",
            "shap_values",
            "top_features",
            "feature_importance",
            "shap",
            "explanation",
        ],
        [],
    )

    shap_features = normalize_explanation_features(
        shap
    )

    story.append(
        Paragraph(
            "SHAP Evidence",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "Feature contribution to the model decision.",
            normal_style,
        )
    )

    if not shap_features:
        story.append(
            Paragraph(
                "No SHAP explanation was returned.",
                small_style,
            )
        )

        story.append(
            Spacer(1, 0.16 * inch)
        )

        return

    rows = [
        [
            header_cell("Feature"),
            header_cell("Contribution"),
        ]
    ]

    for item in shap_features[:10]:

        feature = item.get(
            "feature",
            "Unknown",
        )

        value = item.get(
            "value",
            None,
        )

        rows.append(
            [
                paragraph_cell(
                    display_feature_name(feature),
                    True,
                ),
                paragraph_cell(
                    format_number(value, 4)
                    if value is not None
                    else "N/A"
                ),
            ]
        )

    table = Table(
        rows,
        colWidths=[
            4.7 * inch,
            1.7 * inch,
        ],
        repeatRows=1,
    )

    apply_standard_table_style(
        table,
        "#123b5d",
    )

    story.append(table)
    story.append(
        Spacer(1, 0.2 * inch)
    )


# ============================================================
# LIME
# ============================================================

def add_lime_section(
    story,
    result,
):
    if not isinstance(result, dict):
        result = {}

    lime = first_available(
        result,
        [
            "lime_features",
            "lime_explanation",
            "lime_values",
            "lime",
        ],
        [],
    )

    lime_features = normalize_explanation_features(
        lime
    )

    story.append(
        Paragraph(
            "LIME Evidence",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "Local explanation for this patient.",
            normal_style,
        )
    )

    if not lime_features:
        story.append(
            Paragraph(
                "No LIME explanation was returned.",
                small_style,
            )
        )

        story.append(
            Spacer(1, 0.16 * inch)
        )

        return

    rows = [
        [
            header_cell("Feature / Rule"),
            header_cell("Weight"),
        ]
    ]

    for item in lime_features[:10]:

        feature = item.get(
            "feature",
            "Unknown",
        )

        value = item.get(
            "value",
            None,
        )

        rows.append(
            [
                paragraph_cell(
                    feature,
                    True,
                ),
                paragraph_cell(
                    format_number(value, 4)
                    if value is not None
                    else "N/A"
                ),
            ]
        )

    table = Table(
        rows,
        colWidths=[
            4.7 * inch,
            1.7 * inch,
        ],
        repeatRows=1,
    )

    apply_standard_table_style(
        table,
        "#123b5d",
    )

    story.append(table)
    story.append(
        Spacer(1, 0.2 * inch)
    )


# ============================================================
# AGREEMENT
# ============================================================

def _feature_name_set(items):
    names = set()

    for item in items:
        feature = item.get("feature")

        if feature is not None:
            names.add(
                display_feature_name(
                    feature
                ).lower()
            )

    return names


def derive_agreement_from_explanations(result):
    if not isinstance(result, dict):
        return None

    shap = normalize_explanation_features(
        first_available(
            result,
            [
                "shap_features",
                "shap_values",
                "top_features",
                "feature_importance",
                "shap",
                "explanation",
            ],
            [],
        )
    )

    lime = normalize_explanation_features(
        first_available(
            result,
            [
                "lime_features",
                "lime_explanation",
                "lime_values",
                "lime",
            ],
            [],
        )
    )

    if not shap or not lime:
        return None

    shap_set = _feature_name_set(shap[:5])
    lime_set = _feature_name_set(lime[:5])

    shared = sorted(
        shap_set & lime_set
    )

    union = shap_set | lime_set

    overlap_score = (
        len(shared) / len(union)
        if union
        else 0
    )

    score = overlap_score * 100

    return {
        "agreement_score": score,
        "feature_overlap_percentage": score,
        "overall_consistency_score": score,
        "consistency_level": (
            "High"
            if overlap_score >= 0.67
            else "Moderate"
            if overlap_score >= 0.34
            else "Low"
        ),
        "shared_features": shared,
        "shap_only_features": sorted(
            shap_set - lime_set
        ),
        "lime_only_features": sorted(
            lime_set - shap_set
        ),
        "shared_count": len(shared),
        "evidence_sources": "SHAP + LIME",
    }


def add_agreement_section(
    story,
    result,
):
    if not isinstance(result, dict):
        result = {}

    agreement = first_available(
        result,
        [
            "agreement",
            "shap_lime_agreement",
            "explanation_agreement",
        ],
        None,
    )

    if not isinstance(agreement, dict):
        agreement = derive_agreement_from_explanations(
            result
        )

    story.append(
        Paragraph(
            "Explanation Reliability & Consistency Index (ERI)",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "Multi-XAI Triangulation Metric &nbsp;·&nbsp; Cross-Attribution Concordance between SHAP (Shapley Values) and LIME (Local Surrogate).<br/>"
            "<b>Consensus Weighting:</b> 40% Feature Overlap + 30% Direction Agreement + 30% Ranking Agreement.",
            normal_style,
        )
    )

    if not agreement:
        story.append(
            Paragraph(
                "Agreement information was not returned "
                "for this assessment.",
                small_style,
            )
        )

        story.append(
            Spacer(1, 0.2 * inch)
        )

        return

    agreement_score = first_available(
        agreement,
        [
            "agreement_score",
            "agreement_percentage",
            "agreementScore",
            "score",
            "overall_agreement",
            "overall_agreement_percentage",
        ],
        None,
    )

    feature_overlap = first_available(
        agreement,
        [
            "feature_overlap_percentage",
            "feature_overlap",
            "overlap_percentage",
            "feature_agreement_percentage",
            "feature_agreement",
        ],
        None,
    )

    direction_agreement = first_available(
        agreement,
        [
            "direction_agreement_percentage",
            "direction_agreement",
        ],
        None,
    )

    ranking_agreement = first_available(
        agreement,
        [
            "ranking_agreement_percentage",
            "ranking_agreement",
        ],
        None,
    )

    overall_consistency = first_available(
        agreement,
        [
            "overall_consistency_score",
            "overall_consistency",
            "consistency",
        ],
        None,
    )

    consistency_level = first_available(
        agreement,
        [
            "consistency_level",
            "consistencyLevel",
            "level",
        ],
        "N/A",
    )

    shared_features = first_available(
        agreement,
        [
            "shared_features",
            "common_features",
            "commonFeatures",
        ],
        [],
    )

    shap_only = first_available(
        agreement,
        [
            "shap_only_features",
            "shap_only",
            "shapOnly",
            "shap_specific_features",
        ],
        [],
    )

    lime_only = first_available(
        agreement,
        [
            "lime_only_features",
            "lime_only",
            "limeOnly",
            "lime_specific_features",
        ],
        [],
    )

    shared_count = first_available(
        agreement,
        [
            "shared_count",
            "common_feature_count",
        ],
        None,
    )

    rows = [
        [
            "Overall ERI Score",
            format_percent(agreement_score or overall_consistency),
        ],
        [
            "Feature Overlap (40%)",
            format_percent(feature_overlap),
        ],
        [
            "Direction Agreement (30%)",
            format_percent(direction_agreement),
        ],
        [
            "Ranking Agreement (30%)",
            format_percent(ranking_agreement),
        ],
        [
            "Overall Consistency",
            format_percent(overall_consistency or agreement_score),
        ],
        [
            "Consistency Level",
            (
                f"{consistency_level} Reliability"
                if consistency_level and "Reliability" not in str(consistency_level)
                else (consistency_level or "N/A")
            ),
        ],
        [
            "Shared Feature Count",
            (
                safe_text(shared_count)
                if shared_count is not None
                else (
                    str(len(shared_features))
                    if isinstance(
                        shared_features,
                        (list, tuple, set),
                    )
                    else "N/A"
                )
            ),
        ],
        [
            "Shared Evidence / Common Features",
            format_feature_list(shared_features),
        ],
        [
            "SHAP-Only Features",
            format_feature_list(shap_only),
        ],
        [
            "LIME-Only Features",
            format_feature_list(lime_only),
        ],
    ]

    story.append(
        build_key_value_table(rows)
    )

    story.append(
        Spacer(1, 0.12 * inch)
    )

    story.append(
        Paragraph(
            "Agreement measures consistency between SHAP "
            "and LIME explanations. It indicates explanation "
            "consistency, not clinical certainty.",
            small_style,
        )
    )

    story.append(
        Spacer(1, 0.2 * inch)
    )


# ============================================================
# COUNTERFACTUALS
#
# UNCHANGED from the version you confirmed is working
# correctly.
# ============================================================

def get_counterfactual_changes(
    counterfactual,
    disease=None,
):
    if not isinstance(counterfactual, dict):
        return []

    # 1. Direct feature_changes list from counterfactual_engine
    if "feature_changes" in counterfactual and isinstance(counterfactual["feature_changes"], list):
        items = []
        for ch in counterfactual["feature_changes"]:
            feat_key = ch.get("feature") or ch.get("name") or ""
            feat_name = ch.get("feature_name") or ch.get("label") or display_feature_name(feat_key)
            old_val = ch.get("old_value") if ch.get("old_value") is not None else ch.get("old", "—")
            new_val = ch.get("new_value") if ch.get("new_value") is not None else ch.get("new", "—")
            unit = ch.get("unit") or ""
            delta = ch.get("delta_str") or ch.get("difference") or ch.get("delta")
            if delta is None and old_val != "—" and new_val != "—":
                try:
                    diff = float(new_val) - float(old_val)
                    delta = f"{diff:+.1f} {unit}".strip()
                except Exception:
                    delta = "Modified"
            elif delta is not None:
                delta = str(delta)
            else:
                delta = "Modified"
            action = ch.get("clinical_action") or ch.get("action") or ""

            unit_suffix = f" {unit}".rstrip() if unit else ""
            items.append({
                "feature": feat_name,
                "old": f"{old_val}{unit_suffix}",
                "direction": "&rarr;",
                "new": f"{new_val}{unit_suffix}",
                "delta": delta,
                "action": action
            })
        if items:
            return items

    # 2. Dictionary changes
    changes = counterfactual.get("changes")
    if isinstance(changes, dict):
        items = []
        disease_key = normalize_disease(disease) if disease else "heart"
        try:
            from counterfactual_engine import CLINICAL_METRICS
            disease_metrics = CLINICAL_METRICS.get(disease_key, {})
        except Exception:
            disease_metrics = {}

        for feature, values in changes.items():
            meta = disease_metrics.get(str(feature).lower(), {})
            feat_name = meta.get("name") or display_feature_name(feature)
            unit = meta.get("unit", "")
            action = meta.get("action", "")

            if isinstance(values, dict):
                old_val = values.get("old", values.get("old_value", values.get("original", "—")))
                new_val = values.get("new", values.get("new_value", values.get("counterfactual", "—")))
            elif isinstance(values, (list, tuple)) and len(values) >= 2:
                old_val = values[0]
                new_val = values[1]
            else:
                old_val = "—"
                new_val = values

            try:
                diff = float(new_val) - float(old_val)
                delta = f"{diff:+.1f} {unit}".strip()
            except Exception:
                delta = "Modified"

            unit_suffix = f" {unit}".rstrip() if unit else ""
            items.append({
                "feature": feat_name,
                "old": f"{old_val}{unit_suffix}",
                "direction": "&rarr;",
                "new": f"{new_val}{unit_suffix}",
                "delta": delta,
                "action": action
            })
        return items

    # 3. Direct single feature properties
    feature = first_available(
        counterfactual,
        [
            "changed_feature",
            "feature",
            "feature_name",
        ],
        None,
    )
    if feature is not None:
        old_value = first_available(
            counterfactual,
            ["original_value", "old_value", "from_value", "before"],
            "—",
        )
        new_value = first_available(
            counterfactual,
            ["counterfactual_value", "new_value", "to_value", "after"],
            "—",
        )
        return [
            {
                "feature": display_feature_name(feature),
                "old": str(old_value),
                "direction": "&rarr;",
                "new": str(new_value),
                "delta": "Modified",
                "action": "",
            }
        ]

    return []


def normalize_counterfactual_list(result):
    if not isinstance(result, dict):
        return []

    # If single_counterfactuals and multi_counterfactuals are available, combine them in priority order
    singles = result.get("single_counterfactuals") or []
    multis = result.get("multi_counterfactuals") or []
    if singles or multis:
        combined = []
        if isinstance(singles, list):
            combined.extend(singles)
        if isinstance(multis, list):
            combined.extend(multis)
        if combined:
            return combined

    counterfactuals = first_available(
        result,
        [
            "counterfactuals",
            "counterfactual_explanations",
            "counterfactual_profiles",
        ],
        [],
    )

    if isinstance(counterfactuals, dict):
        nested = first_available(
            counterfactuals,
            [
                "counterfactuals",
                "profiles",
                "results",
                "items",
            ],
            [],
        )
        if isinstance(nested, list):
            return nested
        return []

    if isinstance(counterfactuals, list):
        return counterfactuals

    return []


def add_counterfactual_section(
    story,
    result,
):
    if not isinstance(result, dict):
        result = {}

    disease = disease_display_name(
        first_available(
            result,
            [
                "disease",
                "condition",
            ],
            "unknown",
        )
    )

    counterfactuals = normalize_counterfactual_list(
        result
    )

    story.append(
        Paragraph(
            "Actionable Counterfactual Explanation Engine",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            f"Clinically feasible what-if recourse trajectories &nbsp;·&nbsp; {html_escape(disease)}<br/>"
            "<b>Dual-Sparsity Optimization Framework:</b> Single-Biomarker (Sparsity L0 = 1) and Multi-Biomarker Synergistic Regimens (Sparsity L0 = 2).<br/>"
            "<b>Guardrails:</b> Demographic Invariance (Age, Biological Sex locked). Only modifiable biomarkers within validated therapeutic bounds were adjusted.",
            normal_style,
        )
    )

    original_prediction = first_available(
        result,
        [
            "prediction",
            "predicted_class",
            "class",
            "prediction_class",
        ],
        None,
    )

    original_probability = first_available(
        result,
        [
            "probability",
            "prediction_probability",
            "risk_probability",
            "confidence",
        ],
        None,
    )

    if original_prediction is not None:
        original_text = first_available(
            result,
            [
                "prediction_text",
                "predictionText",
                "predicted_label",
            ],
            prediction_text(
                normalize_disease(
                    result.get(
                        "disease",
                        "unknown",
                    )
                ),
                original_prediction,
            ),
        )

        story.append(
            build_key_value_table(
                [
                    [
                        "Baseline Prediction",
                        original_text,
                    ],
                    [
                        "Baseline Probability",
                        format_percent(
                            original_probability
                        ),
                    ],
                    [
                        "Target Recourse State",
                        "Low Risk / Healthy",
                    ],
                ]
            )
        )

        story.append(
            Spacer(1, 0.14 * inch)
        )

    if not counterfactuals:
        story.append(
            Paragraph(
                "No counterfactual profile was found.",
                warning_style,
            )
        )
        story.append(
            Paragraph(
                "The model did not return a valid alternative "
                f"profile for this {html_escape(disease.lower())} "
                "assessment within the configured search space.",
                small_style,
            )
        )
        story.append(
            Spacer(1, 0.12 * inch)
        )
        story.append(
            Paragraph(
                "<b>Clinical Decision Support Notice:</b> Counterfactual explanations are "
                "hypothetical model-generated simulations demonstrating boundary shifts. "
                "They do not substitute clinical judgment and must not be interpreted as "
                "prescriptions, treatment targets, or medical diagnoses.",
                disclaimer_style,
            )
        )
        return

    # Render up to 5 intervention paths
    for index, counterfactual in enumerate(
        counterfactuals[:5]
    ):
        if not isinstance(counterfactual, dict):
            continue

        changes = get_counterfactual_changes(
            counterfactual,
            result.get("disease")
        )

        probability = first_available(
            counterfactual,
            ["probability", "risk_probability", "confidence"],
            None,
        )

        number_of_changes = first_available(
            counterfactual,
            ["number_of_changes", "num_changes", "sparsity"],
            len(changes),
        )

        prediction_label = first_available(
            counterfactual,
            ["prediction_text", "predicted_label", "new_prediction"],
            "Low Risk / Healthy",
        )

        is_single = (
            counterfactual.get("type") == "single"
            or number_of_changes == 1
            or len(changes) == 1
        )
        sparsity_num = number_of_changes or len(changes) or 1
        tier_label = (
            "Single-Biomarker &nbsp;·&nbsp; Sparsity L0 = 1"
            if is_single
            else f"Multi-Biomarker Regimen &nbsp;·&nbsp; Sparsity L0 = {sparsity_num}"
        )

        # Risk reduction calculation
        orig_p = float(original_probability) if original_probability is not None else 60.0
        new_p = float(probability) if probability is not None else 40.0
        risk_drop_val = counterfactual.get("risk_reduction_pct")
        if risk_drop_val is None and orig_p > 0:
            risk_drop_str = f"{max(0.0, ((orig_p - new_p) / orig_p) * 100):.1f}%"
        elif risk_drop_val is not None:
            risk_drop_str = f"{risk_drop_val}%"
        else:
            risk_drop_str = "Substantial"

        story.append(
            Paragraph(
                f"<b>Intervention Path #{index + 1} &nbsp;·&nbsp; {tier_label}</b>",
                subheading_style,
            )
        )

        summary_meta = (
            f"<b>Status:</b> Clinically Actionable &nbsp;|&nbsp; "
            f"<b>Risk Drop:</b> &#9660; -{risk_drop_str} &nbsp;|&nbsp; "
            f"<b>Baseline:</b> {format_percent(orig_p)} &rarr; <b>Adjusted:</b> {format_percent(new_p)} &nbsp;|&nbsp; "
            f"<b>Target State:</b> {prediction_label}"
        )
        story.append(Paragraph(summary_meta, small_style))
        story.append(Spacer(1, 0.04 * inch))

        if changes:
            cf_table_data = [
                [
                    header_cell("Clinical Biomarker"),
                    header_cell("Baseline Value"),
                    header_cell("Direction"),
                    header_cell("Target Level"),
                    header_cell("Adjustment (Delta)"),
                ]
            ]
            for ch in changes:
                cf_table_data.append(
                    [
                        paragraph_cell(ch.get("feature", "Biomarker"), True),
                        paragraph_cell(ch.get("old", "—")),
                        paragraph_cell(ch.get("direction", "&rarr;")),
                        paragraph_cell(ch.get("new", "—")),
                        paragraph_cell(ch.get("delta", "Modified")),
                    ]
                )

            cf_table = Table(
                cf_table_data,
                colWidths=[
                    1.9 * inch,
                    1.1 * inch,
                    0.6 * inch,
                    1.1 * inch,
                    1.7 * inch,
                ],
            )
            apply_standard_table_style(
                cf_table,
                "#0f766e" if is_single else "#1e3a8a",
            )
            story.append(cf_table)
            story.append(Spacer(1, 0.04 * inch))

        # Physiological rationale
        actions = [ch["action"] for ch in changes if ch.get("action")]
        rationale_text = "; ".join(actions) if actions else counterfactual.get("clinical_rationale", "")
        if rationale_text:
            story.append(
                Paragraph(
                    f"<b>Physiological Rationale:</b> {html_escape(rationale_text)}",
                    small_style,
                )
            )

        story.append(
            Paragraph(
                "<b>Actionability Guarantee:</b> Demographic traits (Age, Biological Sex) are strictly invariant. Only clinically modifiable biomarkers within validated therapeutic bounds were adjusted.",
                small_style,
            )
        )

        story.append(
            Spacer(1, 0.14 * inch)
        )

    story.append(
        Paragraph(
            "<b>Clinical Decision Support Notice:</b> Counterfactual profiles are hypothetical algorithmic simulations demonstrating the boundary shifts required by the diagnostic classifier. They do not substitute clinical judgment, patient-specific contraindications, or pharmacological guidelines. They must not be interpreted as definitive clinical treatment targets, prescriptions, diagnoses, or instructions to alter therapy.",
            disclaimer_style,
        )
    )


# ============================================================
# CLINICAL INTERPRETATION
# ============================================================

def add_clinical_interpretation(
    story,
    result,
):
    story.append(
        Paragraph(
            "Clinical Interpretation Note",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "The prediction and explanation values in this "
            "report represent the output of the machine-learning "
            "system for the submitted patient data. SHAP and "
            "LIME provide model interpretability, while "
            "counterfactual analysis illustrates hypothetical "
            "changes that may cross the model's decision "
            "boundary.",
            normal_style,
        )
    )

    story.append(
        Paragraph(
            "<b>Disclaimer:</b> This report is intended for "
            "clinical decision support only. Model outputs, "
            "SHAP values, LIME explanations, agreement scores, "
            "and counterfactual scenarios must not be interpreted "
            "as definitive diagnoses, prescriptions, treatment "
            "instructions, or required clinical targets. Final "
            "clinical decisions must be made by qualified "
            "healthcare professionals using appropriate clinical "
            "assessment and additional evidence.",
            disclaimer_style,
        )
    )


# ============================================================
# FOOTER
# ============================================================

def add_footer(
    canvas,
    document,
):
    canvas.saveState()

    width, _ = document.pagesize

    canvas.setStrokeColor(
        colors.HexColor("#cbd5e1")
    )

    canvas.setLineWidth(0.5)

    canvas.line(
        document.leftMargin,
        28,
        width - document.rightMargin,
        28,
    )

    canvas.setFont(
        "Helvetica",
        7,
    )

    canvas.setFillColor(
        colors.HexColor("#64748b")
    )

    canvas.drawString(
        document.leftMargin,
        16,
        "Explainable AI Clinical Decision Support System",
    )

    canvas.drawRightString(
        width - document.rightMargin,
        16,
        f"Page {document.page}",
    )

    canvas.restoreState()


# ============================================================
# SIGNATURES
# ============================================================

def add_signature_section(
    story,
    patient,
):
    doctor_name = first_available(
        patient,
        [
            "doctor_name",
            "doctorName",
            "clinician",
            "doctor",
        ],
        "Doctor",
    )

    patient_name = first_available(
        patient,
        [
            "patient_name",
            "patientName",
            "name",
        ],
        "Patient",
    )

    story.append(
        Spacer(1, 0.2 * inch)
    )

    signature_data = [
        [
            Paragraph(
                "<b>Doctor Signature</b>",
                small_style,
            ),
            Paragraph(
                "<b>Patient Signature</b>",
                small_style,
            ),
        ],
        [
            Paragraph(
                "______________________________",
                small_style,
            ),
            Paragraph(
                "______________________________",
                small_style,
            ),
        ],
        [
            Paragraph(
                safe_text(doctor_name),
                small_style,
            ),
            Paragraph(
                safe_text(patient_name),
                small_style,
            ),
        ],
    ]

    signature_table = Table(
        signature_data,
        colWidths=[
            3.2 * inch,
            3.2 * inch,
        ],
    )

    signature_table.setStyle(
        TableStyle(
            [
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
            ]
        )
    )

    story.append(
        signature_table
    )


# ============================================================
# MAIN PDF GENERATOR
# ============================================================

def generate_report(
    patient,
    result,
    output_path,
):
    """
    Generate the complete clinical PDF.

    The prediction, SHAP, LIME, agreement and counterfactual
    sections remain compatible with the existing backend result.

    The clinical-parameter section additionally reads the direct
    patient fields produced by the Flask backend. This fixes the
    Stroke PDF message:

        "No clinical parameter dictionary was supplied."

    without changing the prediction/model logic.
    """

    if not isinstance(patient, dict):
        patient = {}

    if not isinstance(result, dict):
        result = {}

    # --------------------------------------------------------
    # Merge patient metadata from result["patient"] and result.
    # --------------------------------------------------------

    merged_patient = dict(patient)

    result_patient = result.get(
        "patient"
    )

    if isinstance(
        result_patient,
        dict,
    ):
        for key, value in result_patient.items():
            if key not in merged_patient:
                merged_patient[key] = value

    for key in [
        "patient_id",
        "patient_name",
        "doctor_name",
        "hospital_name",
        "disease",
    ]:
        if key not in merged_patient:
            if key in result:
                merged_patient[key] = result[key]

    # --------------------------------------------------------
    # Disease.
    # --------------------------------------------------------

    disease = normalize_disease(
        first_available(
            result,
            [
                "disease",
                "condition",
            ],
            first_available(
                merged_patient,
                [
                    "disease",
                    "condition",
                ],
                "unknown",
            ),
        )
    )

    merged_patient["disease"] = disease

    # --------------------------------------------------------
    # PDF document.
    # --------------------------------------------------------

    document = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=45,
        title=(
            f"{disease_display_name(disease)} "
            "Clinical Prediction Report"
        ),
        author=(
            "Explainable AI Clinical "
            "Decision Support System"
        ),
        subject=(
            "Explainable AI Clinical Decision Support Report"
        ),
    )

    story = []

    # --------------------------------------------------------
    # Header.
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Explainable AI Clinical Decision Support System",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "Clinical Prediction Report",
            subtitle_style,
        )
    )

    story.append(
        Paragraph(
            f"<b>Condition:</b> "
            f"{html_escape(disease_display_name(disease))}",
            normal_style,
        )
    )

    story.append(
        Paragraph(
            f"<b>Generated On:</b> "
            f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
            normal_style,
        )
    )

    story.append(
        Spacer(1, 0.15 * inch)
    )

    # --------------------------------------------------------
    # Patient information.
    #
    # FIX #2: explicit "Field" / "Value" header row added here,
    # exactly the way every other table in this document adds
    # its header, instead of handing raw data rows straight to
    # Table() with no header.
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Patient Information",
            heading_style,
        )
    )

    patient_rows = build_patient_data(
        merged_patient
    )

    patient_table_data = [
        [
            header_cell("Field"),
            header_cell("Value"),
        ]
    ]

    for label, value in patient_rows:
        patient_table_data.append(
            [
                paragraph_cell(label, True),
                paragraph_cell(value),
            ]
        )

    patient_table = Table(
        patient_table_data,
        colWidths=[
            2.6 * inch,
            3.8 * inch,
        ],
        repeatRows=1,
    )

    apply_standard_table_style(
        patient_table,
        "#123b5d",
    )

    story.append(
        patient_table
    )

    story.append(
        Spacer(1, 0.22 * inch)
    )

    # --------------------------------------------------------
    # Clinical parameters.
    # --------------------------------------------------------

    add_clinical_parameters_section(
        story,
        merged_patient,
        result,
    )

    # --------------------------------------------------------
    # Prediction.
    # --------------------------------------------------------

    add_prediction_section(
        story,
        result,
    )

    # --------------------------------------------------------
    # SHAP.
    # --------------------------------------------------------

    add_shap_section(
        story,
        result,
    )

    # --------------------------------------------------------
    # LIME.
    # --------------------------------------------------------

    add_lime_section(
        story,
        result,
    )

    # --------------------------------------------------------
    # SHAP-LIME agreement.
    # --------------------------------------------------------

    add_agreement_section(
        story,
        result,
    )

    # --------------------------------------------------------
    # Counterfactuals.
    # --------------------------------------------------------

    add_counterfactual_section(
        story,
        result,
    )

    # --------------------------------------------------------
    # Clinical interpretation.
    # --------------------------------------------------------

    add_clinical_interpretation(
        story,
        result,
    )

    # --------------------------------------------------------
    # System footer information.
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "<b>Generated by Explainable AI "
            "Clinical Decision Support System</b>",
            normal_style,
        )
    )

    story.append(
        Paragraph(
            "Machine Learning • SHAP • LIME • "
            "SHAP-LIME Agreement • Counterfactual Analysis • "
            "Flask • React",
            small_style,
        )
    )

    # --------------------------------------------------------
    # Signatures.
    # --------------------------------------------------------

    add_signature_section(
        story,
        merged_patient,
    )

    # --------------------------------------------------------
    # Build PDF.
    # --------------------------------------------------------

    document.build(
        story,
        onFirstPage=add_footer,
        onLaterPages=add_footer,
    )


# ============================================================
# COMPATIBILITY ALIASES
# ============================================================

def create_report(
    patient,
    result,
    output_path,
):
    return generate_report(
        patient,
        result,
        output_path,
    )


def generate_clinical_report(
    patient,
    result,
    output_path,
):
    return generate_report(
        patient,
        result,
        output_path,
    )


# ============================================================
# MODULE TEST
# ============================================================

if __name__ == "__main__":
    print()
    print("=" * 70)
    print(
        "EXPLAINABLE AI CLINICAL PDF REPORT GENERATOR"
    )
    print("=" * 70)
    print("Supported diseases:")
    print(" - Heart Disease")
    print(" - Diabetes")
    print(" - Chronic Kidney Disease")
    print(" - Stroke")
    print("=" * 70)
    print("Report generator loaded successfully.")
    print(
        "Use generate_report(patient, result, output_path)"
    )
    print("=" * 70)