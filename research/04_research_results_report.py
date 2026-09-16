"""
04_research_results_report.py

Reads research/results CSV files and creates:
- paper/research_results_report.md
- paper/research_results_table.csv

No model execution and no project-code modification.
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS = PROJECT_ROOT / "research" / "results"
PAPER = PROJECT_ROOT / "paper"
PAPER.mkdir(parents=True, exist_ok=True)

summary_path = RESULTS / "full_research_summary.csv"
stability_path = RESULTS / "explanation_stability_summary.csv"

summary = pd.read_csv(summary_path) if summary_path.exists() else pd.DataFrame()
stability = pd.read_csv(stability_path) if stability_path.exists() else pd.DataFrame()

lines = []
lines.append("# XAI-CDSS Research Results\n")
lines.append("Generated automatically from local experimental outputs. Values are not invented.\n")

if not stability.empty:
    lines.append("## Explanation Stability\n")
    cols = [c for c in [
        "Disease","disease","Patients","patients","Perturbations","perturbations",
        "SHAP_Overlap","SHAP_Spearman","SHAP_Sign","LIME_Overlap","LIME_Spearman","LIME_Sign"
    ] if c in stability.columns]
    lines.append(stability[cols].to_markdown(index=False))
    lines.append("")

if not summary.empty:
    lines.append("## Dataset-Level Agreement and Counterfactual Evaluation\n")
    lines.append(summary.to_markdown(index=False))
    lines.append("")

    for _, r in summary.iterrows():
        disease = r.get("disease", "unknown")
        lines.append(f"### {str(disease).title()}\n")
        lines.append(
            f"- Patients evaluated: {r.get('patients_evaluated', 'N/A')}\n"
            f"- Mean feature agreement: {r.get('mean_feature_agreement_pct', 'N/A'):.2f}%\n"
            f"- Mean direction agreement: {r.get('mean_direction_agreement_pct', 'N/A'):.2f}%\n"
            f"- Mean ranking agreement: {r.get('mean_ranking_agreement_pct', 'N/A'):.2f}%\n"
            f"- Mean overall consistency: {r.get('mean_overall_consistency_pct', 'N/A'):.2f}%\n"
            f"- Counterfactual success rate: {r.get('counterfactual_success_rate_pct', 'N/A'):.2f}%\n"
            f"- Mean SHAP-counterfactual alignment: {r.get('mean_shap_cf_alignment_pct', 'N/A'):.2f}%\n"
            f"- Mean LIME-counterfactual alignment: {r.get('mean_lime_cf_alignment_pct', 'N/A'):.2f}%\n"
        )
else:
    lines.append("## Dataset-Level Evaluation\n")
    lines.append("Run `python research\\03_full_research_evaluation.py` first.\n")

lines.append("## Research Contribution Wording\n")
lines.append(
    "> We propose a unified explanation-reliability framework for tabular clinical decision support "
    "that jointly evaluates model predictions, local feature attributions from SHAP and LIME, "
    "cross-explainer agreement, explanation stability under controlled perturbations, and "
    "model-validated counterfactual decision-boundary behavior. The framework further measures "
    "the alignment between influential explanation features and features involved in successful "
    "counterfactual transitions."
)
lines.append("\n## Limitations\n")
lines.append(
    "- Counterfactuals are model-based what-if scenarios and are not clinical treatment recommendations.\n"
    "- The current perturbation experiment is a local robustness/stability stress test, not external clinical validation.\n"
    "- Agreement indicates consistency between explanation methods; it does not by itself establish causal correctness.\n"
    "- Any novelty statement should use 'we propose' or 'we introduce' unless established by a systematic literature review.\n"
)

(PAPER / "research_results_report.md").write_text("\n".join(lines), encoding="utf-8")
if not summary.empty:
    summary.to_csv(PAPER / "research_results_table.csv", index=False)

print("Generated:", PAPER / "research_results_report.md")
if not summary.empty:
    print("Generated:", PAPER / "research_results_table.csv")
