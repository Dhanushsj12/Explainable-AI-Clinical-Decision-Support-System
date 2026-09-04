import os
import numpy as np
import pandas as pd

from lime.lime_tabular import LimeTabularExplainer

from model_loader import (
    heart_model,
    heart_scaler,
    diabetes_model,
    diabetes_scaler
)


# ==========================================
# Base Directory
# ==========================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)


# ==========================================
# Heart Disease LIME
# ==========================================

heart_df = pd.read_csv(
    os.path.join(
        BASE_DIR,
        "datasets",
        "processed",
        "heart_preprocessed.csv"
    )
)

heart_X_train = heart_df.drop("target", axis=1)

heart_X_train_scaled = heart_scaler.transform(
    heart_X_train
)

heart_feature_names = heart_X_train.columns.tolist()


heart_explainer = LimeTabularExplainer(

    training_data=heart_X_train_scaled,

    feature_names=heart_feature_names,

    class_names=[
        "No Heart Disease",
        "Heart Disease"
    ],

    mode="classification",

    random_state=42
)


# ==========================================
# Diabetes LIME
# ==========================================

diabetes_df = pd.read_csv(
    os.path.join(
        BASE_DIR,
        "datasets",
        "processed",
        "diabetes",
        "x_train.csv"
    )
)

diabetes_X_train_scaled = diabetes_df

diabetes_feature_names = diabetes_df.columns.tolist()


diabetes_explainer = LimeTabularExplainer(

    training_data=diabetes_X_train_scaled.values,

    feature_names=diabetes_feature_names,

    class_names=[
        "Negative",
        "Positive"
    ],

    mode="classification",

    random_state=42
)


# ==========================================
# LIME Function
# ==========================================

def lime_explain(features, disease="heart"):

    patient = np.array(features).reshape(1, -1)


    # ======================================
    # Heart Disease
    # ======================================

    if disease == "heart":

        patient_scaled = heart_scaler.transform(
            patient
        )

        explanation = heart_explainer.explain_instance(

            patient_scaled[0],

            heart_model.predict_proba,

            num_features=5
        )


    # ======================================
    # Diabetes
    # ======================================

    elif disease == "diabetes":

        patient_scaled = diabetes_scaler.transform(
            patient
        )

        explanation = diabetes_explainer.explain_instance(

            patient_scaled[0],

            diabetes_model.predict_proba,

            num_features=5
        )


    else:

        raise ValueError(
            f"Unsupported disease: {disease}"
        )


    # ======================================
    # Convert Explanation
    # ======================================

    result = []

    for feature, weight in explanation.as_list():

        result.append({

            "feature": feature,

            "impact": round(
                float(weight),
                4
            )

        })


    return result