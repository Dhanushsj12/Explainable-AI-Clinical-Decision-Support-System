import pandas as pd

from lime.lime_tabular import LimeTabularExplainer

from model_loader import model, scaler

# ==========================================
# Load Training Data
# ==========================================

df = pd.read_csv(
    "../datasets/processed/heart_preprocessed.csv"
)

X_train = df.drop("target", axis=1)

# ==========================================
# Scale Training Data
# ==========================================

X_train_scaled = scaler.transform(X_train)

# ==========================================
# Feature Names
# ==========================================

feature_names = X_train.columns.tolist()

# ==========================================
# Create LIME Explainer
# ==========================================

explainer = LimeTabularExplainer(

    training_data=X_train_scaled,

    feature_names=feature_names,

    class_names=[
        "No Heart Disease",
        "Heart Disease"
    ],

    mode="classification"

)

# ==========================================
# Explain One Patient
# ==========================================

def lime_explain(features):

    import numpy as np

    patient = np.array(features).reshape(1, -1)

    patient = scaler.transform(patient)

    explanation = explainer.explain_instance(

        patient[0],

        model.predict_proba,

        num_features=5

    )

    result = []

    for feature, weight in explanation.as_list():

        result.append({

            "feature": feature,

            "impact": round(weight, 4)

        })

    return result