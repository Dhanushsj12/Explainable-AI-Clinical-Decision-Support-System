from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

styles = getSampleStyleSheet()


def generate_report(result, output_path):

    document = SimpleDocTemplate(output_path)

    story = []

    story.append(Paragraph("<b>Clinical Decision Support Report</b>", styles["Heading1"]))

    story.append(Paragraph(f"<b>Prediction:</b> {result['prediction']}", styles["BodyText"]))

    story.append(Paragraph(f"<b>Probability:</b> {result['probability']}%", styles["BodyText"]))

    story.append(Paragraph(f"<b>Risk Level:</b> {result['risk_level']}", styles["BodyText"]))

    story.append(Paragraph(f"<b>Recommendation:</b> {result['recommendation']}", styles["BodyText"]))

    story.append(Paragraph("<b>Top Features</b>", styles["Heading2"]))

    for feature in result["top_features"]:
        story.append(
            Paragraph(
                f"{feature['feature']} : {feature['impact']}",
                styles["BodyText"]
            )
        )

    document.build(story)

    return output_path