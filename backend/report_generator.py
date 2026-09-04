from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch

from datetime import datetime


# ==========================================
# Styles
# ==========================================

styles = getSampleStyleSheet()

title_style = styles["Heading1"]
title_style.alignment = TA_CENTER

heading_style = styles["Heading2"]

normal_style = styles["BodyText"]


# ==========================================
# PDF Generator
# ==========================================

def generate_report(patient, result, output_path):

    document = SimpleDocTemplate(
        output_path
    )

    story = []


    # ======================================
    # Title
    # ======================================

    story.append(
        Paragraph(
            "Explainable AI Clinical Decision Support System",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Clinical Prediction Report",
            heading_style
        )
    )

    story.append(
        Spacer(
            1,
            0.3 * inch
        )
    )


    # ======================================
    # Date
    # ======================================

    story.append(
        Paragraph(
            f"<b>Generated On:</b> "
            f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
            normal_style
        )
    )

    story.append(
        Spacer(
            1,
            0.25 * inch
        )
    )


    # ======================================
    # Patient Information
    # ======================================

    story.append(
        Paragraph(
            "Patient Information",
            heading_style
        )
    )


    patient_data = [

        [
            "Patient ID",
            patient.get("patient_id", "")
        ],

        [
            "Patient Name",
            patient.get("patient_name", "")
        ],

        [
            "Doctor",
            patient.get("doctor_name", "")
        ],

        [
            "Hospital",
            patient.get("hospital_name", "")
        ],

        [
            "Disease",
            patient.get("disease", "")
        ]

    ]


    # ======================================
    # Heart Disease Fields
    # ======================================

    if patient.get("disease") == "Heart Disease":

        patient_data.extend([

            [
                "Age",
                patient.get("age", "")
            ],

            [
                "Gender",
                patient.get("gender", "")
            ],

            [
                "Chest Pain Type",
                patient.get("cp", "")
            ],

            [
                "Resting Blood Pressure",
                f"{patient.get('trestbps', '')} mmHg"
            ],

            [
                "Cholesterol",
                f"{patient.get('chol', '')} mg/dL"
            ],

            [
                "Fasting Blood Sugar",
                patient.get("fbs", "")
            ],

            [
                "Rest ECG",
                patient.get("restecg", "")
            ],

            [
                "Maximum Heart Rate",
                patient.get("thalach", "")
            ],

            [
                "Exercise Angina",
                patient.get("exang", "")
            ],

            [
                "ST Depression",
                patient.get("oldpeak", "")
            ],

            [
                "ST Segment Slope",
                patient.get("slope", "")
            ],

            [
                "Major Vessels",
                patient.get("ca", "")
            ],

            [
                "Thalassemia",
                patient.get("thal", "")
            ]

        ])


    # ======================================
    # Diabetes Fields
    # ======================================

    elif patient.get("disease") == "Diabetes":

        diabetes_labels = {

            "age":
                "Age",

            "gender":
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

        }


        for key, label in diabetes_labels.items():

            patient_data.append([

                label,

                patient.get(key, "")

            ])

    # ======================================
    # CKD Fields
    # ======================================

    elif str(patient.get("disease", "")).lower() in ["ckd", "chronic kidney disease"]:

        ckd_labels = {

            "age": "Age",
            "bp": "Blood Pressure",
            "sg": "Specific Gravity",
            "al": "Albumin",
            "su": "Sugar",
            "rbc": "Red Blood Cells",
            "pc": "Pus Cell",
            "pcc": "Pus Cell Clumps",
            "ba": "Bacteria",
            "bgr": "Blood Glucose Random",
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
            "ane": "Anemia"

        }

        for key, label in ckd_labels.items():

            patient_data.append([

                label,

                patient.get(key, "")

            ])

    # ======================================
    # Patient Table
    # ======================================

    patient_table = Table(
        patient_data
    )

    patient_table.setStyle(
        TableStyle([

            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.grey
            ),

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.lightblue
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, -1),
                "Helvetica"
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8
            )

        ])
    )

    story.append(
        patient_table
    )

    story.append(
        Spacer(
            1,
            0.3 * inch
        )
    )


    # ======================================
    # Prediction Result
    # ======================================

    story.append(
        Paragraph(
            "Prediction Result",
            heading_style
        )
    )


    prediction_table = Table([

        [
            "Prediction",
            result["prediction"]
        ],

        [
            "Probability",
            f"{result['probability']} %"
        ],

        [
            "Risk Level",
            result["risk_level"]
        ]

    ])


    prediction_table.setStyle(
        TableStyle([

            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.grey
            ),

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.lightgreen
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8
            )

        ])
    )


    story.append(
        prediction_table
    )

    story.append(
        Spacer(
            1,
            0.3 * inch
        )
    )


    # ======================================
    # Recommendation
    # ======================================

    story.append(
        Paragraph(
            "Clinical Recommendation",
            heading_style
        )
    )

    story.append(
        Paragraph(
            result["recommendation"],
            normal_style
        )
    )

    story.append(
        Spacer(
            1,
            0.3 * inch
        )
    )


    # ======================================
    # SHAP Explanation
    # ======================================

    story.append(
        Paragraph(
            "Top Influencing Features (SHAP)",
            heading_style
        )
    )


    feature_data = [
        ["Feature", "Impact"]
    ]


    for feature in result.get(
        "top_features",
        []
    ):

        feature_data.append([

            feature["feature"],

            str(
                round(
                    feature["impact"],
                    4
                )
            )

        ])


    feature_table = Table(
        feature_data
    )


    feature_table.setStyle(
        TableStyle([

            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black
            ),

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.darkblue
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "BACKGROUND",
                (0, 1),
                (-1, -1),
                colors.beige
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8
            )

        ])
    )


    story.append(
        feature_table
    )

    story.append(
        Spacer(
            1,
            0.4 * inch
        )
    )


    # ======================================
    # LIME Explanation
    # ======================================

    story.append(
        Paragraph(
            "LIME Explanation",
            heading_style
        )
    )


    lime_data = [
        ["Feature", "Impact"]
    ]


    if "lime_features" in result:

        for feature in result["lime_features"]:

            lime_data.append([

                feature["feature"],

                str(
                    round(
                        feature["impact"],
                        4
                    )
                )

            ])


        lime_table = Table(
            lime_data
        )


        lime_table.setStyle(
            TableStyle([

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black
                ),

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.orange
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),

                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.beige
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                )

            ])
        )


        story.append(
            lime_table
        )


    else:

        story.append(
            Paragraph(
                "LIME explanation is not available "
                "for this prediction.",
                normal_style
            )
        )


    story.append(
        Spacer(
            1,
            0.4 * inch
        )
    )


    # ======================================
    # Footer
    # ======================================

    story.append(
        Paragraph(
            "<b>Generated by Explainable AI "
            "Clinical Decision Support System</b>",
            normal_style
        )
    )

    story.append(
        Paragraph(
            "Machine Learning • SHAP • LIME • Flask • React",
            normal_style
        )
    )


    # ======================================
    # Signatures
    # ======================================

    story.append(
        Spacer(
            1,
            0.4 * inch
        )
    )

    story.append(
        Paragraph(
            "<b>Doctor Signature:</b> "
            "__________________________",
            normal_style
        )
    )

    story.append(
        Spacer(
            1,
            0.2 * inch
        )
    )

    story.append(
        Paragraph(
            "<b>Patient Signature:</b> "
            "__________________________",
            normal_style
        )
    )


    # ======================================
    # Build PDF
    # ======================================

    document.build(
        story
    )

    return output_path