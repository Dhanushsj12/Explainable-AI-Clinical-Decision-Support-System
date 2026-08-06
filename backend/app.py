from flask import Flask, request, jsonify
from prediction import predict

app = Flask(__name__)

@app.route("/")
def home():

    return jsonify({
        "project":"Explainable AI CDSS",
        "status":"Running"
    })

@app.route("/predict", methods=["POST"])
def prediction():

    data = request.get_json()

    result = predict(data["features"])

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)