def recommendation(prediction, probability):

    if prediction == 0:

        return {
            "risk": "Low",
            "recommendation":
            "No significant indication of heart disease was detected. Maintain a healthy lifestyle, exercise regularly, and undergo routine medical check-ups."
        }

    elif probability < 70:

        return {
            "risk": "Moderate",
            "recommendation":
            "There are signs associated with heart disease. Consult a cardiologist and undergo additional clinical evaluation."
        }

    else:

        return {
            "risk": "High",
            "recommendation":
            "High likelihood of heart disease. Immediate consultation with a cardiologist is strongly recommended. Further diagnostic tests such as ECG, Echocardiogram, or Angiography may be required."
        }