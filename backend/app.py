from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from prediction import predict
from explainability import explain
from lime_explain import lime_explain
from recommendation import recommendation
from report_generator import generate_report
from database import create_table, save_prediction, get_predictions
import os

app = Flask(__name__)

CORS(app)
create_table()
# ==========================================
# Convert Feature Values to Readable Labels
# ==========================================

def build_patient_data(data, features):

    return {

        "patient_id": data.get("patient_id", ""),

        "patient_name": data.get("patient_name", ""),

        "doctor_name": data.get("doctor_name", ""),

        "hospital_name": data.get("hospital_name", ""),

        "age": features[0],

        "gender": "Male" if features[1] == 1 else "Female",

        "cp": {
            1: "Typical Angina",
            2: "Atypical Angina",
            3: "Non-anginal Pain",
            4: "Asymptomatic"
        }.get(features[2], str(features[2])),

        "trestbps": features[3],

        "chol": features[4],

        "fbs": "Yes" if features[5] == 1 else "No",

        "restecg": {
            0: "Normal",
            1: "ST-T Wave Abnormality",
            2: "Left Ventricular Hypertrophy"
        }.get(features[6], str(features[6])),

        "thalach": features[7],

        "exang": "Yes" if features[8] == 1 else "No",

        "oldpeak": features[9],

        "slope": {
            1: "Upsloping",
            2: "Flat",
            3: "Downsloping"
        }.get(features[10], str(features[10])),

        "ca": features[11],

        "thal": {
            3: "Normal",
            6: "Fixed Defect",
            7: "Reversible Defect"
        }.get(features[12], str(features[12]))

    }

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

# SHAP Explanation
    explanation = explain(features)

# LIME Explanation
    lime = lime_explain(features)

    advice = recommendation(
        result["prediction_class"],
        result["probability"]
    )

    result["risk_level"] = advice["risk"]

    result["recommendation"] = advice["recommendation"]

    result["top_features"] = explanation
    result["lime_features"] = lime
    patient = build_patient_data(data, features)

    save_prediction(
        patient,
        result
)

    return jsonify(result)

@app.route("/report", methods=["POST"])
def report():

    data = request.get_json()


    print("Received from frontend:", data)

    if "features" not in data:
       return jsonify({"error": "Missing 'features' field"}), 400

    features = data["features"]

    # -----------------------------
    # Prediction
    # -----------------------------

    result = predict(features)

    # -----------------------------
    # Explainability
    # -----------------------------

    
    # SHAP
    explanation = explain(features)

# LIME
    lime = lime_explain(features)
    # -----------------------------
    # Recommendation
    # -----------------------------

    advice = recommendation(
        result["prediction_class"],
        result["probability"]
    )

    result["risk_level"] = advice["risk"]

    result["recommendation"] = advice["recommendation"]

    result["top_features"] = explanation
    result["lime_features"] = lime

    # -----------------------------
    # Build Patient Details
    # -----------------------------

    patient = build_patient_data(
        data,
        features
    )

    # -----------------------------
    # Generate PDF
    # -----------------------------

    os.makedirs("reports", exist_ok=True)

    output_path = os.path.join(
        "reports",
        "clinical_report.pdf"
    )

    generate_report(
        patient,
        result,
        output_path
    )

    # -----------------------------
    # Download PDF
    # -----------------------------

    return send_file(
        output_path,
        as_attachment=True,
        download_name="Clinical_Report.pdf"
    )

@app.route("/history", methods=["GET"])
def history():

    history = get_predictions()

    return jsonify(history)
if __name__ == "__main__":
    app.run(debug=True)