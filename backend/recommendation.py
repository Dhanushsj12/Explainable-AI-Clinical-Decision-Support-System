def recommendation(prediction, probability, disease="heart"):

    # ==========================================
    # Heart Disease
    # ==========================================

    if disease == "heart":

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


    # ==========================================
    # Diabetes
    # ==========================================

    elif disease == "diabetes":

        if prediction == 0:

            return {
                "risk": "Low",
                "recommendation":
                "No significant indication of diabetes was detected. Maintain a balanced diet, exercise regularly, and continue routine health check-ups."
            }

        elif probability < 70:

            return {
                "risk": "Moderate",
                "recommendation":
                "The prediction indicates some signs associated with diabetes. Consultation with a healthcare professional and further clinical evaluation are recommended."
            }

        else:

            return {
                "risk": "High",
                "recommendation":
                "High likelihood of diabetes. Consultation with a healthcare professional is strongly recommended for further clinical evaluation and appropriate diagnostic testing."
            }


    # ==========================================
    # Unsupported Disease
    # ==========================================

    else:

        raise ValueError(
            f"Unsupported disease: {disease}"
        )