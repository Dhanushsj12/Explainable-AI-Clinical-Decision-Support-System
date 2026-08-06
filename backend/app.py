from flask import Flask, request, jsonify, send_file

from prediction import predict
from explainability import explain
from recommendation import recommendation
from report_generator import generate_report

import os

app = Flask(__name__)


@app.route("/")
def home():

    return jsonify({
        "project": "Explainable AI Clinical Decision Support System",
        "status": "Running",
        "version": "1.0"
    })


@app.route("/predict", methods=["POST"])
def prediction():

    data = request.get_json()

    if "features" not in data:
        return jsonify({"error": "Missing 'features' field"}), 400

    features = data["features"]

    result = predict(features)

    explanation = explain(features)

    advice = recommendation(
        result["prediction_class"],
        result["probability"]
    )

    result["risk_level"] = advice["risk"]

    result["recommendation"] = advice["recommendation"]

    result["top_features"] = explanation

    return jsonify(result)


@app.route("/report", methods=["POST"])
def report():

    data = request.get_json()

    if "features" not in data:
        return jsonify({"error": "Missing 'features' field"}), 400

    features = data["features"]

    result = predict(features)

    explanation = explain(features)

    advice = recommendation(
        result["prediction_class"],
        result["probability"]
    )

    result["risk_level"] = advice["risk"]

    result["recommendation"] = advice["recommendation"]

    result["top_features"] = explanation

    output_path = os.path.join("reports", "clinical_report.pdf")

    os.makedirs("reports", exist_ok=True)

    generate_report(result, output_path)

    return send_file(
        output_path,
        as_attachment=True,
        download_name="Clinical_Report.pdf"
    )


if __name__ == "__main__":
    app.run(debug=True)