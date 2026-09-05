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
        output_path,
        pagesize=(8.27 * inch, 11.69 * inch),
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
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
        Spacer(1, 0.25 * inch)
    )

    # ======================================
    # Generated Date
    # ======================================

    story.append(
        Paragraph(
            f"<b>Generated On:</b> "
            f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
            normal_style
        )
    )

    story.append(
        Spacer(1, 0.25 * inch)
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
        ["Field", "Value"],

        [
            "Patient ID",
            str(patient.get("patient_id", ""))
        ],

        [
            "Patient Name",
            str(patient.get("patient_name", ""))
        ],

        [
            "Doctor",
            str(patient.get("doctor_name", ""))
        ],

        [
            "Hospital",
            str(patient.get("hospital_name", ""))
        ],

        [
            "Disease",
            str(patient.get("disease", ""))
        ]
    ]

    # ======================================
    # Heart Disease Fields
    # ======================================

    if patient.get("disease") == "Heart Disease":

        patient_data.extend([

            ["Age", str(patient.get("age", ""))],

            ["Gender", str(patient.get("gender", ""))],

            ["Chest Pain Type", str(patient.get("cp", ""))],

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
                str(patient.get("fbs", ""))
            ],

            [
                "Rest ECG",
                str(patient.get("restecg", ""))
            ],

            [
                "Maximum Heart Rate",
                str(patient.get("thalach", ""))
            ],

            [
                "Exercise Angina",
                str(patient.get("exang", ""))
            ],

            [
                "ST Depression",
                str(patient.get("oldpeak", ""))
            ],

            [
                "ST Segment Slope",
                str(patient.get("slope", ""))
            ],

            [
                "Major Vessels",
                str(patient.get("ca", ""))
            ],

            [
                "Thalassemia",
                str(patient.get("thal", ""))
            ]
        ])

    # ======================================
    # Diabetes Fields
    # ======================================

    elif patient.get("disease") == "Diabetes":

        diabetes_labels = {

            "age": "Age",
            "gender": "Gender",
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
            "obesity": "Obesity"

        }

        for key, label in diabetes_labels.items():

            patient_data.append([
                label,
                str(patient.get(key, ""))
            ])

    # ======================================
    # CKD Fields
    # ======================================

    elif str(patient.get("disease", "")).lower() in [
        "ckd",
        "chronic kidney disease"
    ]:

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
                str(patient.get(key, ""))
            ])

    # ======================================
    # Stroke Fields
    # ======================================

    elif str(patient.get("disease", "")).lower() == "stroke":

        stroke_labels = {

            "age": "Age",

            "gender": "Gender",

            "hypertension": "Hypertension",

            "heart_disease": "Heart Disease",

            "ever_married": "Ever Married",

            "work_type": "Work Type",

            "Residence_type": "Residence Type",

            "avg_glucose_level": "Average Glucose Level",

            "bmi": "Body Mass Index (BMI)",

            "smoking_status": "Smoking Status"

        }

        for key, label in stroke_labels.items():

            value = patient.get(key, "")

            # Format numerical values nicely
            if key == "avg_glucose_level":
                try:
                    value = f"{float(value):.2f}"
                except:
                    pass

            elif key == "bmi":
                try:
                    value = f"{float(value):.1f}"
                except:
                    pass

            elif key in ["hypertension", "heart_disease"]:

                if str(value) == "1":
                    value = "Yes"

                elif str(value) == "0":
                    value = "No"

            patient_data.append([
                label,
                str(value)
            ])

    # ======================================
    # Patient Information Table
    # ======================================

    patient_table = Table(
        patient_data,
        colWidths=[2.6 * inch, 3.8 * inch],
        repeatRows=1
    )

    patient_table.setStyle(
        TableStyle([

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.8,
                colors.grey
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
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "BACKGROUND",
                (0, 1),
                (0, -1),
                colors.lightblue
            ),

            (
                "FONTNAME",
                (0, 1),
                (0, -1),
                "Helvetica-Bold"
            ),

            (
                "FONTNAME",
                (1, 1),
                (1, -1),
                "Helvetica"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            )

        ])
    )

    story.append(patient_table)

    story.append(
        Spacer(1, 0.3 * inch)
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

    prediction_table = Table(
        [
            ["Field", "Result"],

            [
                "Prediction",
                str(result.get("prediction", ""))
            ],

            [
                "Probability",
                f"{result.get('probability', '')} %"
            ],

            [
                "Risk Level",
                str(result.get("risk_level", ""))
            ],

            [
                "Prediction Class",
                str(result.get("prediction_class", ""))
            ]

        ],
        colWidths=[2.6 * inch, 3.8 * inch]
    )

    prediction_table.setStyle(
        TableStyle([

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.8,
                colors.grey
            ),

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.darkgreen
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "BACKGROUND",
                (0, 1),
                (0, -1),
                colors.lightgreen
            ),

            (
                "FONTNAME",
                (0, 1),
                (0, -1),
                "Helvetica-Bold"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            )

        ])
    )

    story.append(prediction_table)

    story.append(
        Spacer(1, 0.3 * inch)
    )

    # ======================================
    # Clinical Recommendation
    # ======================================

    story.append(
        Paragraph(
            "Clinical Recommendation",
            heading_style
        )
    )

    story.append(
        Paragraph(
            str(result.get("recommendation", "")),
            normal_style
        )
    )

    story.append(
        Spacer(1, 0.3 * inch)
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

    shap_data = [
        ["Feature", "Impact"]
    ]

    for feature in result.get("top_features", []):

        shap_data.append([
            str(feature.get("feature", "")),
            str(round(float(feature.get("impact", 0)), 4))
        ])

    shap_table = Table(
        shap_data,
        colWidths=[4.8 * inch, 1.6 * inch],
        repeatRows=1
    )

    shap_table.setStyle(
        TableStyle([

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.8,
                colors.grey
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
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "BACKGROUND",
                (0, 1),
                (-1, -1),
                colors.beige
            ),

            (
                "ALIGN",
                (1, 1),
                (1, -1),
                "CENTER"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            )

        ])
    )

    story.append(shap_table)

    story.append(
        Spacer(1, 0.35 * inch)
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

    story.append(
        Paragraph(
            "Local Interpretable Model-Agnostic Explanation "
            "(LIME) showing the most influential conditions "
            "used by the model for this prediction.",
            normal_style
        )
    )

    story.append(
        Spacer(1, 0.15 * inch)
    )

    lime_data = [
        ["Feature", "Impact"]
    ]

    for feature in result.get("lime_features", []):

        lime_data.append([
            str(feature.get("feature", "")),
            str(round(float(feature.get("impact", 0)), 4))
        ])

    if len(lime_data) > 1:

        lime_table = Table(
            lime_data,
            colWidths=[4.8 * inch, 1.6 * inch],
            repeatRows=1
        )

        lime_table.setStyle(
            TableStyle([

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.8,
                    colors.grey
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
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),

                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.beige
                ),

                (
                    "ALIGN",
                    (1, 1),
                    (1, -1),
                    "CENTER"
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )

            ])
        )

        story.append(lime_table)

    else:

        story.append(
            Paragraph(
                "LIME explanation is not available "
                "for this prediction.",
                normal_style
            )
        )

    story.append(
        Spacer(1, 0.4 * inch)
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
        Spacer(1, 0.4 * inch)
    )

    story.append(
        Paragraph(
            "<b>Doctor Signature:</b> "
            "______________________________",
            normal_style
        )
    )

    story.append(
        Spacer(1, 0.2 * inch)
    )

    story.append(
        Paragraph(
            "<b>Patient Signature:</b> "
            "______________________________",
            normal_style
        )
    )

    # ======================================
    # Build PDF
    # ======================================

    document.build(story)

    return output_path