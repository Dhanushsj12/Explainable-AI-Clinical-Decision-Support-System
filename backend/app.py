from flask import Flask, request, jsonify

from prediction import predict
from explainability import explain
from recommendation import recommendation

app = Flask(__name__)


@app.route("/")
def home():

    return jsonify({

        "project":
        "Explainable AI Clinical Decision Support System",

        "status":
        "Running",

        "version":
        "1.0"

    })


@app.route("/predict", methods=["POST"])
def prediction():

    data = request.get_json()

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


if __name__ == "__main__":
    app.run(debug=True)