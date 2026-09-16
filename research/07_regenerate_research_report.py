
"""
07_regenerate_research_report.py

Regenerates the research results report from FINAL CSV outputs.
No model execution.

Run from project root:
    python research\07_regenerate_research_report.py
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "research" / "results"
PAPER = ROOT / "paper"
PAPER.mkdir(parents=True, exist_ok=True)

def read(name):
    path = RESULTS / name
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    df.columns = [str(c).strip().lower() for c in df.columns]
    return df

model = read("model_performance_final.csv")
agreement = read("agreement_final.csv")
cf = read("counterfactual_final.csv")
stability = read("stability_statistics_final.csv")
aug = read("augmentation_heart_final.csv")
baseline = read("baseline_available_final.csv")
ablation = read("ablation_posthoc_final.csv")

lines = []
lines += [
    "# XAI-CDSS Research Results",
    "",
    "Generated from saved experimental outputs only. No models were retrained and no SHAP, LIME, or counterfactual search was rerun during report generation.",
    "",
]

if not model.empty:
    show = [c for c in ["disease","accuracy","precision","recall_sensitivity","specificity","f1","roc_auc","samples","tn","fp","fn","tp"] if c in model.columns]
    lines += ["## Held-out Model Performance", "", model[show].to_markdown(index=False), ""]

if not agreement.empty:
    show = [c for c in ["disease","patients_evaluated","agreement_valid_cases","mean_feature_agreement_pct","mean_direction_agreement_pct","mean_ranking_agreement_pct","mean_overall_consistency_pct"] if c in agreement.columns]
    lines += ["## SHAP–LIME Agreement", "", agreement[show].to_markdown(index=False), ""]

if not cf.empty:
    show = [c for c in ["disease","patients_evaluated","counterfactual_valid_cases","counterfactual_success_cases","counterfactual_success_rate_pct","mean_cf_count","mean_cf_feature_count","mean_shap_cf_alignment_pct","mean_lime_cf_alignment_pct","mean_common_cf_alignment_pct"] if c in cf.columns]
    lines += ["## Counterfactual Evaluation", "", cf[show].to_markdown(index=False), ""]

if not stability.empty:
    lines += ["## Explanation Stability Statistics", ""]
    # Compact table: one row per disease/metric with mean, SD, median, IQR.
    show = [c for c in ["disease","metric","n","mean","std","median","iqr"] if c in stability.columns]
    lines += [stability[show].to_markdown(index=False), ""]

lines += [
    "## Interpretation Notes",
    "",
    "- The held-out model metrics describe the saved production classifiers evaluated on the saved real test sets.",
    "- SHAP–LIME agreement measures consistency between post-hoc explanation methods; agreement does not establish causal correctness.",
    "- Counterfactuals are model-validated what-if scenarios, not clinical treatment recommendations.",
    "- For diseases with zero successful counterfactual cases, SHAP/LIME counterfactual-alignment statistics are reported as N/A rather than zero because no successful counterfactual set exists for comparison.",
    "- The perturbation experiment is a controlled local stability stress test, not external clinical robustness or clinical validation.",
    "- Post-hoc explanation components do not retrain the classifier; therefore their addition should not be described as improving classification accuracy.",
    "- The saved Heart augmentation experiment is reported separately and should not be generalized as an all-disease augmentation comparison.",
    "",
]

if not baseline.empty:
    lines += ["## Available Baseline Evidence", "", baseline.to_markdown(index=False), ""]

if not ablation.empty:
    lines += ["## Post-hoc Component Analysis", "", ablation.to_markdown(index=False), ""]

if not aug.empty:
    lines += ["## Heart Augmentation Experiment", "", aug.to_markdown(index=False), ""]

lines += [
    "## Research Contribution Wording",
    "",
    "> We propose a unified explanation-reliability framework for tabular clinical decision support that jointly evaluates model predictions, local feature attributions from SHAP and LIME, cross-explainer agreement, explanation stability under controlled perturbations, and model-validated counterfactual decision-boundary behavior. The framework further measures the alignment between influential explanation features and features involved in successful counterfactual transitions.",
    "",
    "## Limitations",
    "",
    "- Counterfactuals are model-based what-if scenarios and are not clinical treatment recommendations.",
    "- The current perturbation experiment is a local robustness/stability stress test, not external clinical validation.",
    "- Agreement indicates consistency between explanation methods; it does not by itself establish causal correctness.",
    "- The stability study used 10 real test patients per disease and 5 perturbations per patient; it is a pilot-scale evaluation rather than a large external validation study.",
    "- The saved augmentation comparison is currently available for Heart Disease only.",
    "- Any novelty statement should use cautious wording such as 'we propose' or 'we introduce' unless established by a systematic literature review.",
    "",
]

out = PAPER / "research_results_report.md"
out.write_text("\n".join(lines), encoding="utf-8")

# Also create a compact combined CSV for easy paper table import.
combined = []
if not model.empty:
    tmp = model.copy()
    tmp.insert(0, "table", "model_performance")
    combined.append(tmp)
if not agreement.empty:
    tmp = agreement.copy()
    tmp.insert(0, "table", "agreement")
    combined.append(tmp)
if not cf.empty:
    tmp = cf.copy()
    tmp.insert(0, "table", "counterfactual")
    combined.append(tmp)
if not stability.empty:
    tmp = stability.copy()
    tmp.insert(0, "table", "stability")
    combined.append(tmp)

if combined:
    pd.concat(combined, ignore_index=True, sort=False).to_csv(
        PAPER / "research_results_final_combined.csv", index=False
    )

print("=" * 72)
print("RESEARCH REPORT REGENERATED")
print("=" * 72)
print("Created:", out)
if combined:
    print("Created:", PAPER / "research_results_final_combined.csv")
print("No model execution performed.")
