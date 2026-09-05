import numpy as np

from model_loader import (
    stroke_model,
    stroke_feature_names
)

from explainability import (
    stroke_explainer,
    preprocess_stroke_for_shap
)


# Test patient from your Stroke report
features = {
    "gender": "Male",
    "age": 78,
    "hypertension": 1,
    "heart_disease": 1,
    "ever_married": "Yes",
    "work_type": "Private",
    "Residence_type": "Urban",
    "avg_glucose_level": 245.60,
    "bmi": 34.8,
    "smoking_status": "smokes"
}


# Prepare patient
patient_scaled = preprocess_stroke_for_shap(features)


# Model output
probability = stroke_model.predict_proba(patient_scaled)[0, 1]
decision = stroke_model.decision_function(patient_scaled)[0]


# SHAP output
shap_result = stroke_explainer(patient_scaled)

print("\nSHAP shape:")
print(shap_result.values.shape)

print("\nBase value:")
print(shap_result.base_values)

values = shap_result.values[0]

# IMPORTANT:
# Do not select [:, 1] here.
# Just inspect the actual shape first.

if values.ndim > 1:
    print("\nMultidimensional SHAP output detected.")
    print("Shape:", values.shape)
else:
    print("\nSingle-output SHAP detected.")

print("\n================================")
print("MODEL")
print("================================")

print("Stroke probability:", probability)
print("Probability %:", probability * 100)
print("Decision function:", decision)


print("\n================================")
print("SHAP")
print("================================")

base = shap_result.base_values[0]

if np.ndim(base) > 0:
    print("Base values:", base)
else:
    print("Base value:", base)

print("SHAP values shape:", shap_result.values.shape)


# If single output
if values.ndim == 1:

    shap_sum = base + values.sum()

    print("SHAP sum:", values.sum())
    print("Base + SHAP:", shap_sum)
    print("Model decision:", decision)
    print("Difference:", abs(shap_sum - decision))

    print("\nTop SHAP features:")

    for feature, impact in sorted(
        zip(stroke_feature_names, values),
        key=lambda x: abs(x[1]),
        reverse=True
    )[:10]:

        print(f"{feature:35s} {impact:+.6f}")


print("\n================================")
print("DONE")
print("================================")