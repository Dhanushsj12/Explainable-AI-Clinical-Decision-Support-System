"""
Clinically-Constrained Dual-Tier Counterfactual Explanation Engine
IEEE-Ready Novelty Contribution for Explainable AI Clinical Decision Support

Supports:
  1. Heart Disease (13 features, Random Forest)
  2. Diabetes (16 features, Decision Tree)
  3. Chronic Kidney Disease (24 features, Random Forest)
  4. Stroke Risk (10 features, Logistic Regression with 0.85 threshold)

Features & Novelty:
  - Dual-Tier Classification: Explicitly separates Single-Biomarker Interventions (Sparsity = 1)
    and Multi-Biomarker Regimens (Sparsity = 2 or 3).
  - Strict Immutability Guardrail: Prevents unethical/impossible changes to immutable traits (Age, Sex/Gender, Marital status, etc.).
  - Directional Plausibility & Clinical Actionability: Values only move towards certified healthy medical reference intervals.
  - Granular Delta, Unit, Direction, and Action Rationale included for every suggested change.
"""

import copy
import itertools
import numpy as np
import pandas as pd

from model_loader import (
    heart_model, heart_scaler,
    diabetes_model, diabetes_scaler,
    ckd_model, ckd_scaler,
    stroke_model, stroke_scaler, stroke_imputer, stroke_feature_names, stroke_threshold
)
from prediction import (
    predict,
    HEART_FEATURES,
    CKD_FEATURES,
    STROKE_FEATURES
)

# -------------------------------------------------------------
# FEATURE DEFINITIONS
# -------------------------------------------------------------

DIABETES_FEATURES = [
    "age", "gender", "polyuria", "polydipsia", "sudden_weight_loss",
    "weakness", "polyphagia", "genital_thrush", "visual_blurring",
    "itching", "irritability", "delayed_healing", "partial_paresis",
    "muscle_stiffness", "alopecia", "obesity"
]

FEATURE_NAMES = {
    "heart": HEART_FEATURES,
    "diabetes": DIABETES_FEATURES,
    "ckd": CKD_FEATURES,
    "stroke": STROKE_FEATURES
}

# -------------------------------------------------------------
# IMMUTABLE CLINICAL TRAITS (NEVER ALTER IN COUNTERFACTUALS)
# -------------------------------------------------------------

IMMUTABLE_FEATURES = {
    "heart": {"age", "sex"},
    "diabetes": {"age", "gender"},
    "ckd": {"age"},
    "stroke": {"age", "gender", "ever_married", "work_type", "Residence_type"}
}

# -------------------------------------------------------------
# CLINICAL REFERENCE RANGES, UNITS & INTERVENTION ACTIONS
# -------------------------------------------------------------

CLINICAL_METRICS = {
    "heart": {
        "trestbps": {
            "name": "Resting Blood Pressure",
            "unit": "mmHg",
            "direction": "decrease",
            "healthy": [115, 120, 125],
            "action": "Lower systolic blood pressure to < 120 mmHg via ACE inhibitors/ARBs and DASH dietary plan."
        },
        "chol": {
            "name": "Serum Cholesterol",
            "unit": "mg/dL",
            "direction": "decrease",
            "healthy": [160, 175, 190],
            "action": "Initiate statin therapy and dietary saturated fat reduction to achieve optimal lipid levels."
        },
        "thalach": {
            "name": "Maximum Heart Rate",
            "unit": "bpm",
            "direction": "increase",
            "healthy": [145, 155, 165],
            "action": "Enhance myocardial aerobic capacity and chronotropic reserve through structured cardiac rehab."
        },
        "oldpeak": {
            "name": "ST Depression",
            "unit": "mm",
            "direction": "decrease",
            "healthy": [0.0, 0.2, 0.4],
            "action": "Reduce subendocardial ischemia through coronary perfusion optimization and anti-anginal therapy."
        },
        "cp": {
            "name": "Chest Pain Type",
            "unit": "grade",
            "direction": "decrease",
            "healthy": [0, 1],
            "action": "Relieve myocardial oxygen supply-demand mismatch via medical or revascularization interventions."
        },
        "exang": {
            "name": "Exercise Induced Angina",
            "unit": "",
            "direction": "decrease",
            "healthy": [0],
            "action": "Eliminate exertional chest pain using titrated beta-blockers or calcium channel blockers."
        },
        "slope": {
            "name": "ST Segment Slope",
            "unit": "grade",
            "direction": "decrease",
            "healthy": [0, 1],
            "action": "Normalize exercise electrocardiographic repolarization profile."
        },
        "ca": {
            "name": "Major Vessels Blocked",
            "unit": "vessels",
            "direction": "decrease",
            "healthy": [0],
            "action": "Achieve vessel patency and reduce obstructive plaque burden."
        },
        "thal": {
            "name": "Thalassemia Perfusion",
            "unit": "grade",
            "direction": "decrease",
            "healthy": [1, 2],
            "action": "Restore homogeneous myocardial perfusion on myocardial scintigraphy."
        },
        "fbs": {
            "name": "Fasting Blood Sugar > 120",
            "unit": "",
            "direction": "decrease",
            "healthy": [0],
            "action": "Maintain fasting blood glucose < 100 mg/dL to minimize microvascular endothelial injury."
        },
        "restecg": {
            "name": "Resting ECG",
            "unit": "grade",
            "direction": "decrease",
            "healthy": [0],
            "action": "Maintain normal baseline resting electrocardiogram."
        }
    },
    "diabetes": {
        "polyuria": {
            "name": "Polyuria (Frequent Urination)",
            "unit": "",
            "direction": "decrease",
            "healthy": [0],
            "action": "Resolve osmotic diuresis by lowering blood glucose below renal threshold (180 mg/dL)."
        },
        "polydipsia": {
            "name": "Polydipsia (Excessive Thirst)",
            "unit": "",
            "direction": "decrease",
            "healthy": [0],
            "action": "Eliminate intracellular dehydration driven by persistent hyperglycemia."
        },
        "sudden_weight_loss": {
            "name": "Sudden Weight Loss",
            "unit": "",
            "direction": "decrease",
            "healthy": [0],
            "action": "Restore anabolic insulin signaling to prevent protein catabolism and muscle wasting."
        },
        "weakness": {
            "name": "Fatigue / Generalized Weakness",
            "unit": "",
            "direction": "decrease",
            "healthy": [0],
            "action": "Improve cellular glucose uptake and mitochondrial ATP generation via glycemic control."
        },
        "polyphagia": {
            "name": "Polyphagia (Extreme Hunger)",
            "unit": "",
            "direction": "decrease",
            "healthy": [0],
            "action": "Normalize hypothalamic satiety feedback mechanisms through steady glucose control."
        },
        "genital_thrush": {
            "name": "Genital Thrush",
            "unit": "",
            "direction": "decrease",
            "healthy": [0],
            "action": "Prevent opportunistic candidiasis by eliminating urinary glucose excretion."
        },
        "visual_blurring": {
            "name": "Visual Blurring",
            "unit": "",
            "direction": "decrease",
            "healthy": [0],
            "action": "Reverse osmotic lens swelling and refractive instability via normoglycemia."
        },
        "itching": {
            "name": "Pruritus / Itching",
            "unit": "",
            "direction": "decrease",
            "healthy": [0],
            "action": "Alleviate skin xerosis and microvascular irritation associated with metabolic stress."
        },
        "irritability": {
            "name": "Irritability / Mood Swings",
            "unit": "",
            "direction": "decrease",
            "healthy": [0],
            "action": "Stabilize central nervous system neurotransmission by avoiding hyper/hypoglycemic excursions."
        },
        "delayed_healing": {
            "name": "Delayed Wound Healing",
            "unit": "",
            "direction": "decrease",
            "healthy": [0],
            "action": "Restore neutrophil chemotaxis, collagen synthesis, and peripheral tissue perfusion."
        },
        "partial_paresis": {
            "name": "Partial Paresis / Numbness",
            "unit": "",
            "direction": "decrease",
            "healthy": [0],
            "action": "Prevent axonal loss and motor nerve conduction impairment through neurovascular support."
        },
        "muscle_stiffness": {
            "name": "Muscle Stiffness",
            "unit": "",
            "direction": "decrease",
            "healthy": [0],
            "action": "Mitigate advanced glycation end-products accumulation in tendons and myofascial layers."
        },
        "alopecia": {
            "name": "Alopecia / Hair Loss",
            "unit": "",
            "direction": "decrease",
            "healthy": [0],
            "action": "Optimize follicle microcirculation and correct underlying systemic metabolic stress."
        },
        "obesity": {
            "name": "Obesity (BMI >= 30)",
            "unit": "",
            "direction": "decrease",
            "healthy": [0],
            "action": "Achieve 7-10% sustained body weight reduction through calorie restriction and physical activity."
        }
    },
    "ckd": {
        "al": {
            "name": "Urine Albumin (Proteinuria)",
            "unit": "grade",
            "direction": "decrease",
            "healthy": [0],
            "action": "Reduce intraglomerular hypertension and podocyte injury via SGLT2 inhibitors or ARB therapy."
        },
        "sc": {
            "name": "Serum Creatinine",
            "unit": "mg/dL",
            "direction": "decrease",
            "healthy": [0.8, 0.9, 1.0, 1.1],
            "action": "Preserve functional nephron filtration rate, optimize renal hemodynamics, and avoid NSAIDs."
        },
        "hemo": {
            "name": "Hemoglobin",
            "unit": "g/dL",
            "direction": "increase",
            "healthy": [14.0, 15.0, 15.8],
            "action": "Correct renal anemia with erythropoiesis-stimulating agents (ESA) and intravenous iron replacement."
        },
        "pcv": {
            "name": "Packed Cell Volume (Hematocrit)",
            "unit": "%",
            "direction": "increase",
            "healthy": [42.0, 45.0, 48.0],
            "action": "Restore circulating red cell mass to improve tissue oxygenation and reduce hyperdynamic cardiac load."
        },
        "sg": {
            "name": "Urine Specific Gravity",
            "unit": "",
            "direction": "increase",
            "healthy": [1.020, 1.025],
            "action": "Recover medullary concentrating gradient and renal tubular absorptive function."
        },
        "bgr": {
            "name": "Blood Glucose Random",
            "unit": "mg/dL",
            "direction": "decrease",
            "healthy": [90.0, 105.0, 120.0],
            "action": "Target HbA1c < 6.5% to prevent diabetic nephropathy progression and mesangial expansion."
        },
        "bu": {
            "name": "Blood Urea",
            "unit": "mg/dL",
            "direction": "decrease",
            "healthy": [18.0, 24.0, 30.0],
            "action": "Lower circulating uremic solute burden via moderate dietary protein management and hydration."
        },
        "bp": {
            "name": "Diastolic Blood Pressure",
            "unit": "mmHg",
            "direction": "decrease",
            "healthy": [70.0, 75.0, 80.0],
            "action": "Strict blood pressure control (< 120/80 mmHg) to attenuate progressive glomerulosclerosis."
        },
        "rbcc": {
            "name": "Red Blood Cell Count",
            "unit": "M/uL",
            "direction": "increase",
            "healthy": [4.8, 5.2, 5.5],
            "action": "Normalize erythrocyte indices and erythropoietin response."
        },
        "htn": {
            "name": "Hypertension History",
            "unit": "",
            "direction": "decrease",
            "healthy": [0],
            "action": "Optimize antihypertensive regimen to achieve target normotension."
        },
        "dm": {
            "name": "Diabetes Mellitus History",
            "unit": "",
            "direction": "decrease",
            "healthy": [0],
            "action": "Tight metabolic glycemic control to prevent progressive microvascular nephrosclerosis."
        },
        "sod": {
            "name": "Serum Sodium",
            "unit": "mEq/L",
            "direction": "optimize",
            "healthy": [138.0, 140.0, 142.0],
            "action": "Maintain electrolyte balance and prevent hyponatremia/hypernatremia."
        },
        "pot": {
            "name": "Serum Potassium",
            "unit": "mEq/L",
            "direction": "optimize",
            "healthy": [4.0, 4.2, 4.5],
            "action": "Maintain serum potassium in safe window (3.5-5.0 mEq/L) via dietary adjustment and binders."
        },
        "pe": {
            "name": "Pedal Edema",
            "unit": "",
            "direction": "decrease",
            "healthy": [0],
            "action": "Relieve peripheral fluid retention with titrated loop diuretics and dietary sodium restriction."
        },
        "ane": {
            "name": "Anemia Clinical Sign",
            "unit": "",
            "direction": "decrease",
            "healthy": [0],
            "action": "Resolution of clinical signs of fatigue, pallor, and tissue hypoxemia."
        }
    },
    "stroke": {
        "avg_glucose_level": {
            "name": "Average Glucose Level",
            "unit": "mg/dL",
            "direction": "decrease",
            "healthy": [85.0, 95.0, 110.0],
            "action": "Normalize glycemic levels to reduce cerebral microvascular endothelial damage and platelet activation."
        },
        "bmi": {
            "name": "Body Mass Index (BMI)",
            "unit": "kg/m²",
            "direction": "decrease",
            "healthy": [22.5, 23.8, 24.9],
            "action": "Target healthy BMI range to mitigate obstructive sleep apnea, arterial stiffness, and systemic inflammation."
        },
        "hypertension": {
            "name": "Hypertension Status",
            "unit": "",
            "direction": "decrease",
            "healthy": [0],
            "action": "Maintain blood pressure < 130/80 mmHg to dramatically lower cerebral infarction and intracranial hemorrhage risk."
        },
        "smoking_status": {
            "name": "Smoking Status",
            "unit": "",
            "direction": "decrease",
            "healthy": ["never smoked"],
            "action": "Complete smoking cessation to eliminate nicotine-induced vasoconstriction and prothrombotic state."
        },
        "heart_disease": {
            "name": "Heart Disease Status",
            "unit": "",
            "direction": "decrease",
            "healthy": [0],
            "action": "Manage cardiac arrhythmias and structural heart conditions to prevent cardioembolic stroke."
        }
    }
}

# -------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------

def normalize_disease_name(disease):
    if disease is None:
        return "heart"
    d = str(disease).strip().lower()
    mapping = {
        "heart": "heart",
        "heart disease": "heart",
        "heart_disease": "heart",
        "cardiac": "heart",
        "diabetes": "diabetes",
        "diabetic": "diabetes",
        "ckd": "ckd",
        "chronic kidney disease": "ckd",
        "chronic_kidney_disease": "ckd",
        "stroke": "stroke"
    }
    return mapping.get(d, d)

def to_feature_dict(features, disease):
    disease = normalize_disease_name(disease)
    names = FEATURE_NAMES.get(disease, [])
    if isinstance(features, dict):
        return {k: features.get(k) for k in names}
    return {name: val for name, val in zip(names, features)}

def to_model_input(p_dict, disease):
    disease = normalize_disease_name(disease)
    names = FEATURE_NAMES.get(disease, [])
    if disease == "stroke":
        return dict(p_dict)
    return [p_dict[name] for name in names]

def eval_patient_state(p_dict, disease):
    inp = to_model_input(p_dict, disease)
    res = predict(inp, disease)
    pred = int(res["prediction_class"])
    raw_prob = float(res["probability"])
    # All prediction functions return a percentage (0 to 100). A value such
    # as 0.79 means 0.79%, not 79%; always convert it to a probability.
    prob = raw_prob / 100.0
    return pred, prob

def format_clinical_delta(old_val, new_val, unit):
    try:
        diff = float(new_val) - float(old_val)
        sign = "+" if diff > 0 else ""
        diff_str = f"{sign}{round(diff, 2)}"
        if unit:
            diff_str += f" {unit}"
        return diff_str
    except Exception:
        return f"{old_val} -> {new_val}"

# -------------------------------------------------------------
# CORE COUNTERFACTUAL GENERATION ENGINE
# -------------------------------------------------------------

def generate_counterfactual_suite(features, disease, max_single=3, max_multi=5):
    """
    Generates a dual-tier counterfactual suite:
      1. Single-Feature Counterfactuals (Sparsity = 1, minimal actionable barrier)
      2. Multi-Feature Counterfactuals (Sparsity = 2 or 3, holistic regimen)
    """
    disease = normalize_disease_name(disease)
    p_dict = to_feature_dict(features, disease)
    orig_pred, orig_prob = eval_patient_state(p_dict, disease)
    target_class = 0 if orig_pred == 1 else 1
    
    immutables = IMMUTABLE_FEATURES.get(disease, set())
    metrics = CLINICAL_METRICS.get(disease, {})
    
    # ---------------------------------------------------------
    # TIER 1: SINGLE-FEATURE COUNTERFACTUAL SEARCH (Sparsity = 1)
    # ---------------------------------------------------------
    single_cfs = []
    single_fallback_pool = []
    
    for feat, meta in metrics.items():
        if feat in immutables:
            continue
        orig_val = p_dict.get(feat)
        for cand_val in meta["healthy"]:
            if str(orig_val) == str(cand_val):
                continue
            cand_dict = copy.deepcopy(p_dict)
            cand_dict[feat] = cand_val
            c_pred, c_prob = eval_patient_state(cand_dict, disease)
            
            diff_val = None
            try:
                diff_val = round(float(cand_val) - float(orig_val), 2)
            except Exception:
                pass
                
            change_obj = {
                "feature": feat,
                "feature_name": meta["name"],
                "label": meta["name"],
                "old_value": orig_val,
                "new_value": cand_val,
                "difference": diff_val,
                "delta_str": format_clinical_delta(orig_val, cand_val, meta["unit"]),
                "unit": meta["unit"],
                "direction": meta["direction"],
                "clinical_action": meta["action"]
            }
            
            record = {
                "type": "single",
                "tier": "Tier 1: Minimal Actionable Intervention",
                "number_of_changes": 1,
                "num_changes": 1,
                "prediction": c_pred,
                "prediction_text": "Low Risk / Healthy" if c_pred == 0 else "Disease Risk Present",
                "probability": round(c_prob * 100, 2),
                "original_probability": round(orig_prob * 100, 2),
                "probability_reduction": round(max(0.0, (orig_prob - c_prob) * 100), 2),
                "changes": {feat: [orig_val, cand_val]},
                "feature_changes": [change_obj],
                "detailed_changes": [change_obj],
                "flips_prediction": (c_pred == target_class),
                "normalized_change": 1.0,
                "clinical_rationale": meta["action"]
            }
            
            if c_pred == target_class:
                single_cfs.append(record)
            else:
                single_fallback_pool.append(record)
                
    # Sort single CFs by resultant probability (lowest risk first)
    single_cfs.sort(key=lambda x: x["probability"])
    
    # If no single feature fully crossed 0.5 (e.g. multi-pathology patient),
    # surface the highest risk-reducing single-step interventions so the doctor has clear guidance
    if not single_cfs and single_fallback_pool:
        single_fallback_pool.sort(key=lambda x: x["probability_reduction"], reverse=True)
        seen_feats = set()
        for cand in single_fallback_pool:
            f = list(cand["changes"].keys())[0]
            if f not in seen_feats and cand["probability_reduction"] > 0:
                seen_feats.add(f)
                cand["note"] = "Maximum single-biomarker therapeutic risk reduction step."
                single_cfs.append(cand)
                if len(single_cfs) >= max_single:
                    break
    single_cfs = single_cfs[:max_single]
    
    # ---------------------------------------------------------
    # TIER 2: MULTI-FEATURE COUNTERFACTUAL SEARCH (Sparsity = 2 or 3)
    # ---------------------------------------------------------
    multi_cfs = []
    candidate_features = [f for f in metrics.keys() if f not in immutables]
    
    pairs = list(itertools.combinations(candidate_features, 2))
    triples = list(itertools.combinations(candidate_features, 3))
    
    def score_combination(combo):
        score = 0
        for f in combo:
            oval = p_dict.get(f)
            meta = metrics[f]
            if str(oval) not in [str(x) for x in meta["healthy"]]:
                score += 2
        return score
        
    pairs.sort(key=score_combination, reverse=True)
    triples.sort(key=score_combination, reverse=True)
    
    multi_fallback_pool = []
    
    # Evaluate prioritized clinical combinations
    search_space = pairs[:70] + triples[:70]
    for combo in search_space:
        val_choices = [metrics[f]["healthy"][:2] for f in combo]
        for vals in itertools.product(*val_choices):
            cand_dict = copy.deepcopy(p_dict)
            changed_items = []
            dict_changes = {}
            for f, val in zip(combo, vals):
                oval = p_dict.get(f)
                if str(oval) == str(val):
                    continue
                cand_dict[f] = val
                dict_changes[f] = [oval, val]
                
                diff_val = None
                try:
                    diff_val = round(float(val) - float(oval), 2)
                except Exception:
                    pass
                    
                changed_items.append({
                    "feature": f,
                    "feature_name": metrics[f]["name"],
                    "label": metrics[f]["name"],
                    "old_value": oval,
                    "new_value": val,
                    "difference": diff_val,
                    "delta_str": format_clinical_delta(oval, val, metrics[f]["unit"]),
                    "unit": metrics[f]["unit"],
                    "direction": metrics[f]["direction"],
                    "clinical_action": metrics[f]["action"]
                })
                
            if len(changed_items) < 2:
                continue
                
            c_pred, c_prob = eval_patient_state(cand_dict, disease)
            
            summary_actions = "; ".join([item["clinical_action"] for item in changed_items])
            
            record = {
                "type": "multi",
                "tier": f"Tier 2: Multi-Factor Synergistic Regimen ({len(changed_items)} Biomarkers)",
                "number_of_changes": len(changed_items),
                "num_changes": len(changed_items),
                "prediction": c_pred,
                "prediction_text": "Low Risk / Healthy" if c_pred == 0 else "Substantial Risk Reduction",
                "probability": round(c_prob * 100, 2),
                "original_probability": round(orig_prob * 100, 2),
                "probability_reduction": round(max(0.0, (orig_prob - c_prob) * 100), 2),
                "changes": dict_changes,
                "feature_changes": changed_items,
                "detailed_changes": changed_items,
                "flips_prediction": (c_pred == target_class),
                "normalized_change": float(len(changed_items)),
                "clinical_rationale": summary_actions
            }
            
            if c_pred == target_class:
                multi_cfs.append(record)
            else:
                multi_fallback_pool.append(record)
                
            if len(multi_cfs) >= 20:
                break
        if len(multi_cfs) >= 20:
            break
            
    multi_cfs.sort(key=lambda x: (x["number_of_changes"], x["probability"]))
    
    if not multi_cfs and multi_fallback_pool:
        multi_fallback_pool.sort(key=lambda x: x["probability_reduction"], reverse=True)
        seen_keys = set()
        for cand in multi_fallback_pool:
            k = tuple(sorted(cand["changes"].keys()))
            if k not in seen_keys and cand["probability_reduction"] > 0:
                seen_keys.add(k)
                cand["note"] = "Synergistic multi-biomarker regimen yielding maximum therapeutic risk drop."
                multi_cfs.append(cand)
                if len(multi_cfs) >= max_multi:
                    break
    multi_cfs = multi_cfs[:max_multi]
    
    # Combined ranked list (Single first, then Multi)
    combined_all = single_cfs + multi_cfs
    
    return {
        "disease": disease,
        "original_prediction": orig_pred,
        "original_probability": round(orig_prob * 100, 2),
        "target_prediction": target_class,
        "target_text": "Low Risk / Healthy" if target_class == 0 else "Disease Risk Present",
        "single_counterfactuals": single_cfs,
        "multi_counterfactuals": multi_cfs,
        "counterfactuals": combined_all,
        "total_counterfactuals": len(combined_all),
        "novelty_metadata": {
            "engine": "Dual-Tier Clinically-Constrained Counterfactual Engine",
            "sparsity_framework": "Single-Biomarker (Minimal Effort) vs. Multi-Biomarker (Synergistic Regimen)",
            "immutable_guardrails_enforced": list(immutables),
            "medical_plausibility_enforced": True
        }
    }

# -------------------------------------------------------------
# BACKWARD COMPATIBILITY WRAPPERS
# -------------------------------------------------------------

def find_counterfactuals(patient, disease="heart", max_results=5, max_features_changed=2):
    res = generate_counterfactual_suite(patient, disease)
    cfs = res.get("counterfactuals", [])[:max_results]
    return res.get("original_prediction", 0), res.get("original_probability", 0.0), cfs

def find_heart_counterfactuals(features, max_results=5):
    return find_counterfactuals(features, "heart", max_results=max_results)

def find_diabetes_counterfactuals(features, max_results=5):
    return find_counterfactuals(features, "diabetes", max_results=max_results)

def find_ckd_counterfactuals(features, max_results=5):
    return find_counterfactuals(features, "ckd", max_results=max_results)

def find_stroke_counterfactuals(features, max_results=5):
    return find_counterfactuals(features, "stroke", max_results=max_results)

def normalize_counterfactuals(counterfactuals, disease):
    if isinstance(counterfactuals, dict) and "counterfactuals" in counterfactuals:
        return counterfactuals["counterfactuals"]
    if isinstance(counterfactuals, list):
        return counterfactuals
    return []


# ---------------------------------------------------------------------------
# Direction-aware counterfactual implementation.
#
# The older implementation selected every class-flipping candidate as if a
# lower positive-class probability were always desirable. That is wrong for a
# low-risk patient, where a counterfactual is a risk-increasing sensitivity
# scenario, and it allowed risk-increasing recommendations for high-risk
# patients. This replacement evaluates every candidate with the production
# prediction function and keeps only candidates whose probability moves in the
# requested direction.
# ---------------------------------------------------------------------------

RISK_TEST_VALUES = {
    "heart": {
        "trestbps": [140, 160, 180], "chol": [240, 280, 320],
        "thalach": [125, 105, 90], "oldpeak": [1.5, 2.5, 3.5],
        "cp": [2, 3], "exang": [1], "slope": [2], "ca": [1, 2, 3],
        "thal": [3], "fbs": [1], "restecg": [1, 2],
    },
    "diabetes": {name: [1] for name in DIABETES_FEATURES if name not in {"age", "gender"}},
    "ckd": {
        "al": [2, 3, 4], "sc": [2.0, 3.0, 4.0], "hemo": [11.0, 9.0],
        "pcv": [35.0, 28.0], "sg": [1.010, 1.005], "bgr": [160.0, 220.0],
        "bu": [50.0, 80.0], "bp": [90.0, 110.0], "rbcc": [4.0, 3.2],
        "htn": [1], "dm": [1], "sod": [130.0, 148.0], "pot": [5.5, 6.2],
        "pe": [1], "ane": [1],
    },
    "stroke": {
        "avg_glucose_level": [160.0, 210.0, 260.0], "bmi": [30.0, 35.0, 40.0],
        "hypertension": [1], "heart_disease": [1], "smoking_status": ["smokes"],
    },
}


def _counterfactual_prediction_text(disease, prediction):
    if prediction == 1:
        return "Disease Risk Present"
    return "Low Risk / Healthy"


def _candidate_values(disease, feature, original_prediction):
    if original_prediction == 1:
        return CLINICAL_METRICS[disease][feature]["healthy"]
    return RISK_TEST_VALUES.get(disease, {}).get(feature, [])


def _make_directional_record(disease, original, original_prediction, original_probability, changes):
    candidate = dict(original)
    candidate.update({feature: new_value for feature, new_value in changes.items()})
    candidate_prediction, candidate_probability = eval_patient_state(candidate, disease)
    probability_delta = candidate_probability - original_probability
    wants_risk_reduction = original_prediction == 1
    direction_is_valid = probability_delta < -1e-9 if wants_risk_reduction else probability_delta > 1e-9
    if not direction_is_valid:
        return None

    target_prediction = 0 if wants_risk_reduction else 1
    details = []
    for feature, new_value in changes.items():
        meta = CLINICAL_METRICS[disease][feature]
        old_value = original[feature]
        details.append({
            "feature": feature,
            "feature_name": meta["name"],
            "label": meta["name"],
            "old_value": old_value,
            "new_value": new_value,
            "difference": round(float(new_value) - float(old_value), 3) if isinstance(new_value, (int, float, np.number)) and isinstance(old_value, (int, float, np.number)) else None,
            "delta_str": format_clinical_delta(old_value, new_value, meta["unit"]),
            "unit": meta["unit"],
            "direction": meta["direction"],
            "clinical_action": meta["action"],
        })

    flips_prediction = candidate_prediction == target_prediction
    # A low-risk patient's intentionally risk-increasing inputs are sensitivity
    # tests, even when they cross the classifier boundary. They are never
    # presented as clinical interventions or recommendations.
    is_sensitivity = original_prediction == 0 or not flips_prediction
    probability_change = round(probability_delta * 100, 2)
    return {
        "type": "sensitivity" if is_sensitivity else "counterfactual",
        "tier": "Clinical risk-reduction counterfactual" if not is_sensitivity else "Risk-increasing model sensitivity scenario (not clinical advice)",
        "number_of_changes": len(changes),
        "num_changes": len(changes),
        "prediction": candidate_prediction,
        "prediction_text": _counterfactual_prediction_text(disease, candidate_prediction),
        "probability": round(candidate_probability * 100, 2),
        "original_probability": round(original_probability * 100, 2),
        "probability_change": probability_change,
        "probability_reduction": round(max(0.0, -probability_delta * 100), 2),
        "probability_increase": round(max(0.0, probability_delta * 100), 2),
        "changes": {feature: [original[feature], value] for feature, value in changes.items()},
        "feature_changes": details,
        "detailed_changes": details,
        "flips_prediction": flips_prediction,
        "normalized_change": float(len(changes)),
        "clinical_rationale": "; ".join(item["clinical_action"] for item in details) if not is_sensitivity else "Hypothetical model sensitivity scenario only. It is not a clinical recommendation.",
        "note": "Risk-increasing scenario for model sensitivity only; do not interpret it as clinical advice." if original_prediction == 0 else (None if flips_prediction else "This reduces risk but does not cross the deployed model's decision threshold."),
    }


def generate_counterfactual_suite(features, disease, max_single=3, max_multi=5):
    """Return verified, directionally correct counterfactuals for one patient."""
    disease = normalize_disease_name(disease)
    original = to_feature_dict(features, disease)
    original_prediction, original_probability = eval_patient_state(original, disease)
    target_prediction = 0 if original_prediction == 1 else 1
    mutable = [
        feature for feature in CLINICAL_METRICS.get(disease, {})
        if feature not in IMMUTABLE_FEATURES.get(disease, set()) and feature in original
    ]

    single_candidates = []
    for feature in mutable:
        for value in _candidate_values(disease, feature, original_prediction):
            if str(value) == str(original.get(feature)):
                continue
            record = _make_directional_record(
                disease, original, original_prediction, original_probability, {feature: value}
            )
            if record is not None:
                single_candidates.append(record)

    multi_candidates = []
    # Use the first clinically meaningful change for each feature. The search is
    # bounded while still covering all two-feature combinations.
    for first, second in itertools.combinations(mutable, 2):
        first_values = _candidate_values(disease, first, original_prediction)
        second_values = _candidate_values(disease, second, original_prediction)
        if not first_values or not second_values:
            continue
        for first_value, second_value in itertools.product(first_values[:2], second_values[:2]):
            if str(first_value) == str(original.get(first)) or str(second_value) == str(original.get(second)):
                continue
            record = _make_directional_record(
                disease,
                original,
                original_prediction,
                original_probability,
                {first: first_value, second: second_value},
            )
            if record is not None:
                multi_candidates.append(record)

    wants_risk_reduction = original_prediction == 1
    probability_key = (lambda item: item["probability"]) if wants_risk_reduction else (lambda item: -item["probability"])
    single_flips = [item for item in single_candidates if item["flips_prediction"]]
    multi_flips = [item for item in multi_candidates if item["flips_prediction"]]
    single_sensitivity = [item for item in single_candidates if not item["flips_prediction"]]
    multi_sensitivity = [item for item in multi_candidates if not item["flips_prediction"]]
    single_flips.sort(key=probability_key)
    multi_flips.sort(key=probability_key)
    single_sensitivity.sort(key=probability_key)
    multi_sensitivity.sort(key=probability_key)

    # A genuine counterfactual changes class. When no actionable change can
    # cross the model threshold, expose a clearly labelled sensitivity result
    # rather than falsely calling it a class-flipping counterfactual.
    selected_single = (single_flips or single_sensitivity)[:max_single]
    selected_multi = (multi_flips or multi_sensitivity)[:max_multi]
    combined = selected_single + selected_multi
    return {
        "disease": disease,
        "original_prediction": original_prediction,
        "original_probability": round(original_probability * 100, 2),
        "target_prediction": target_prediction,
        "target_text": _counterfactual_prediction_text(disease, target_prediction),
        "single_counterfactuals": selected_single,
        "multi_counterfactuals": selected_multi,
        "counterfactuals": combined,
        "total_counterfactuals": len(combined),
        "genuine_counterfactual_count": len(single_flips) + len(multi_flips),
        "novelty_metadata": {
            "engine": "Direction-aware clinically constrained counterfactual engine",
            "immutable_guardrails_enforced": sorted(IMMUTABLE_FEATURES.get(disease, set())),
            "medical_plausibility_enforced": True,
            "uses_production_decision_threshold": True,
        },
    }
