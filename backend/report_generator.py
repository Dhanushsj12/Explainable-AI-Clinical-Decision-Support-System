"""Generate a concise PDF report from a completed clinical assessment."""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from xml.sax.saxutils import escape


def _text(value):
    return escape(str(value if value not in (None, "") else "Not provided"))


def _section(title, rows, styles):
    data = [[Paragraph(f"<b>{_text(key)}</b>", styles["BodyText"]), Paragraph(_text(value), styles["BodyText"])] for key, value in rows]
    table = Table(data, colWidths=[6.2 * cm, 11.3 * cm], repeatRows=0)
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.35, colors.lightgrey),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F2F6FA")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return [Paragraph(title, styles["Heading2"]), table, Spacer(1, 0.35 * cm)]


def generate_report(patient, result, output_path):
    """Create one portable PDF report. This is an educational project output."""
    styles = getSampleStyleSheet()
    document = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=1.5 * cm, leftMargin=1.5 * cm, topMargin=1.4 * cm, bottomMargin=1.4 * cm)
    story = [
        Paragraph("Explainable Clinical Decision Support System", styles["Title"]),
        Paragraph("Clinical Assessment Report", styles["Heading2"]),
        Spacer(1, 0.25 * cm),
    ]

    patient_rows = [(key.replace("_", " ").title(), value) for key, value in (patient or {}).items() if key != "features"]
    if patient_rows:
        story += _section("Patient Details", patient_rows, styles)

    story += _section("Prediction", [
        ("Disease", result.get("disease", "")),
        ("Result", result.get("prediction", "")),
        ("Probability (%)", result.get("probability", "")),
        ("Recommendation", result.get("recommendation", "")),
    ], styles)

    features = result.get("top_features") or result.get("explanation") or []
    if features:
        story += _section("SHAP Explanation", [(item.get("feature", "Feature"), item.get("impact", "")) for item in features], styles)

    lime_features = result.get("lime_features") or []
    if lime_features:
        story += _section("LIME Explanation", [(item.get("feature", "Feature"), item.get("impact", "")) for item in lime_features], styles)

    agreement = result.get("agreement") or {}
    if agreement:
        story += _section("Cross-Explainer Concordance Index (CECI)", [
            ("CECI score (%)", agreement.get("overall_consistency_score", agreement.get("score", ""))),
            ("Feature overlap (%)", agreement.get("feature_agreement_percentage", "")),
            ("Direction agreement (%)", agreement.get("direction_agreement_percentage", "")),
            ("Ranking agreement (%)", agreement.get("ranking_agreement_percentage", "")),
            ("Consistency level", agreement.get("consistency_level", "")),
        ], styles)

    ara = result.get("ara") or {}
    if ara:
        story += _section("Attribution-to-Recourse Alignment (ARA)", [
            ("SHAP alignment (%)", ara.get("shap_alignment_percentage", "")),
            ("LIME alignment (%)", ara.get("lime_alignment_percentage", "")),
            ("Mean ARA (%)", ara.get("mean_alignment_percentage", "")),
            ("Recourse features", ", ".join(ara.get("recourse_features", []))),
            ("Interpretation", ara.get("note", "")),
        ], styles)

    counterfactuals = result.get("counterfactuals") or []
    if counterfactuals:
        rows = []
        baseline_probability = float(result.get("probability", 0) or 0)
        original_class = int(result.get("prediction_class", 0) or 0)
        for index, item in enumerate(counterfactuals[:5], start=1):
            changes = item.get("changes", {})
            change_text = ", ".join(f"{key}: {value}" for key, value in changes.items())
            probability = float(item.get("probability", 0) or 0)
            is_sensitivity = (
    original_class == 0 or
    item.get("type") == "sensitivity" or
    item.get("flips_prediction") is False
)
            scenario_type = "Risk-increasing sensitivity" if is_sensitivity and probability > baseline_probability else (
                "Risk-reducing sensitivity" if is_sensitivity else "Class-changing counterfactual"
            )
            rows.append((
                f"Scenario {index}",
                f"{scenario_type}; probability {item.get('probability', '')}%; {change_text}"
            ))
        story += _section("Counterfactual and Sensitivity Scenarios", rows, styles)

    story.append(Paragraph("This report is generated for academic demonstration only and is not a medical diagnosis.", styles["Italic"]))
    document.build(story)
