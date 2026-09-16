
"""
06_generate_research_figures.py — final corrected version

Reads ONLY existing research CSVs.
No model training, SHAP, LIME, or counterfactual execution.

Fix:
- Disease names are canonicalized across all tables.
- Stability overlap comes from explanation_stability_summary.csv.
- Stability Spearman comes from stability_statistics_final.csv.
"""

from pathlib import Path
import math
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "research" / "results"
FIGURES = ROOT / "paper" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

DISEASES = ["heart", "diabetes", "ckd", "stroke"]
LABELS = {
    "heart": "Heart Disease",
    "diabetes": "Diabetes",
    "ckd": "Chronic Kidney Disease",
    "stroke": "Stroke",
}

def read_csv(name):
    path = RESULTS / name
    if not path.exists():
        raise FileNotFoundError(f"Missing: {path}")
    df = pd.read_csv(path)
    df.columns = [str(c).strip().lower() for c in df.columns]
    return df

def canonical_disease(value):
    s = str(value).strip().lower()
    aliases = {
        "heart": "heart",
        "heart disease": "heart",
        "diabetes": "diabetes",
        "diabetic": "diabetes",
        "ckd": "ckd",
        "chronic kidney disease": "ckd",
        "kidney disease": "ckd",
        "stroke": "stroke",
    }
    return aliases.get(s, s)

def add_disease_key(df):
    df = df.copy()
    if "disease" in df.columns:
        df["disease_key"] = df["disease"].map(canonical_disease)
    return df

def first_value(df, disease, column):
    rows = df[df["disease_key"] == disease]
    if rows.empty or column not in df.columns:
        return math.nan
    value = pd.to_numeric(rows.iloc[0][column], errors="coerce")
    return float(value) if pd.notna(value) else math.nan

def save(fig, filename):
    fig.tight_layout()
    fig.savefig(FIGURES / filename, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("Created:", FIGURES / filename)

print("=" * 72)
print("XAI-CDSS FIGURE GENERATION — FINAL CORRECTED")
print("=" * 72)
print("Existing CSVs only. No model execution.\n")

model = add_disease_key(read_csv("model_performance_final.csv"))
agreement = add_disease_key(read_csv("agreement_final.csv"))
cf = add_disease_key(read_csv("counterfactual_final.csv"))
stability_stats = add_disease_key(read_csv("stability_statistics_final.csv"))
stability_summary = add_disease_key(read_csv("explanation_stability_summary.csv"))
aug = read_csv("augmentation_heart_final.csv")

# Figure 1
metrics = [
    ("accuracy", "Accuracy"),
    ("precision", "Precision"),
    ("recall_sensitivity", "Recall"),
    ("f1", "F1"),
    ("roc_auc", "ROC-AUC"),
]
available = [(c, n) for c, n in metrics if c in model.columns]

fig, ax = plt.subplots(figsize=(11, 6.5))
x = list(range(len(DISEASES)))
width = 0.8 / len(available)

for i, (col, name) in enumerate(available):
    vals = [first_value(model, d, col) * 100 for d in DISEASES]
    offsets = [j + (i - (len(available) - 1) / 2) * width for j in x]
    ax.bar(offsets, vals, width=width, label=name)

ax.set_xticks(x)
ax.set_xticklabels([LABELS[d] for d in DISEASES])
ax.set_ylabel("Score (%)")
ax.set_title("Held-out Test Performance Across Diseases")
ax.set_ylim(0, 105)
ax.legend(ncol=3)
save(fig, "fig1_model_performance.png")

# Figure 2
agreement_metrics = [
    ("mean_feature_agreement_pct", "Feature agreement"),
    ("mean_direction_agreement_pct", "Direction agreement"),
    ("mean_ranking_agreement_pct", "Ranking agreement"),
    ("mean_overall_consistency_pct", "Overall consistency"),
]

fig, ax = plt.subplots(figsize=(11, 6.5))
width = 0.8 / len(agreement_metrics)

for i, (col, name) in enumerate(agreement_metrics):
    vals = [first_value(agreement, d, col) for d in DISEASES]
    offsets = [j + (i - (len(agreement_metrics) - 1) / 2) * width for j in x]
    ax.bar(offsets, vals, width=width, label=name)

ax.set_xticks(x)
ax.set_xticklabels([LABELS[d] for d in DISEASES])
ax.set_ylabel("Agreement / consistency (%)")
ax.set_title("Cross-Explainer SHAP–LIME Agreement")
ax.set_ylim(0, 105)
ax.legend(ncol=2)
save(fig, "fig2_shap_lime_agreement.png")

# Figure 3
fig, ax = plt.subplots(figsize=(10, 6))
vals = [first_value(cf, d, "counterfactual_success_rate_pct") for d in DISEASES]
bars = ax.bar([LABELS[d] for d in DISEASES], vals)
ax.set_ylabel("Successful counterfactual cases (%)")
ax.set_title("Model-Validated Counterfactual Success Rate")
ax.set_ylim(0, 105)

for bar, value in zip(bars, vals):
    if not math.isnan(value):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            (value + 2) if value > 0 else 2,
            f"{value:.1f}%",
            ha="center",
            va="bottom",
        )

save(fig, "fig3_counterfactual_success.png")

# Figure 4 — stability
# Overlap values are stored in explanation_stability_summary.csv.
# Spearman means are stored in stability_statistics_final.csv.
fig, ax = plt.subplots(figsize=(11, 6.5))

stability_metrics = [
    ("SHAP Overlap", "shap overlap"),
    ("LIME Overlap", "lime overlap"),
    ("SHAP Spearman", "shap spearman"),
    ("LIME Spearman", "lime spearman"),
]
width = 0.8 / len(stability_metrics)

for i, (display_name, metric_name) in enumerate(stability_metrics):
    vals = []
    for d in DISEASES:
        if "overlap" in metric_name:
            rows = stability_summary[
                (stability_summary["disease_key"] == d)
                & stability_summary["shap_overlap"].notna()
            ]
            if metric_name == "lime overlap":
                column = "lime_overlap"
            else:
                column = "shap_overlap"
            if rows.empty or column not in stability_summary.columns:
                value = math.nan
            else:
                value = pd.to_numeric(rows.iloc[0][column], errors="coerce")
        else:
            rows = stability_stats[
                (stability_stats["disease_key"] == d)
                & (
                    stability_stats["metric"]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    .eq(metric_name)
                )
            ]
            if rows.empty:
                value = math.nan
            else:
                value = pd.to_numeric(rows.iloc[0]["mean"], errors="coerce")
                if pd.notna(value):
                    value = float(value) * 100

        vals.append(float(value) if pd.notna(value) else math.nan)

    offsets = [j + (i - (len(stability_metrics) - 1) / 2) * width for j in x]
    ax.bar(offsets, vals, width=width, label=display_name)

ax.set_xticks(x)
ax.set_xticklabels([LABELS[d] for d in DISEASES])
ax.set_ylabel("Mean value (%)")
ax.set_title("Explanation Stability Under Controlled Perturbations")
ax.set_ylim(0, 105)
ax.legend(ncol=2)
save(fig, "fig4_explanation_stability.png")

# Figure 5
synthetic_column = next(
    (c for c in ["synthetic rows", "synthetic_rows"] if c in aug.columns),
    None,
)

if synthetic_column:
    metric_candidates = [
        ("accuracy", "Accuracy"),
        ("precision", "Precision"),
        ("f1 score", "F1"),
        ("f1_score", "F1"),
        ("roc-auc", "ROC-AUC"),
        ("roc_auc", "ROC-AUC"),
    ]

    chosen = []
    seen = set()
    for col, name in metric_candidates:
        if col in aug.columns and name not in seen:
            chosen.append((col, name))
            seen.add(name)

    fig, ax = plt.subplots(figsize=(11, 6.5))
    xvals = pd.to_numeric(aug[synthetic_column], errors="coerce")

    for col, name in chosen:
        y = pd.to_numeric(aug[col], errors="coerce") * 100
        ax.plot(xvals, y, marker="o", label=name)

    ax.set_xlabel("Synthetic training rows")
    ax.set_ylabel("Score (%)")
    ax.set_title("Heart Disease Performance vs. Synthetic Data Size")
    ax.set_ylim(0, 105)
    ax.legend()
    save(fig, "fig5_heart_augmentation.png")

print("\nFIGURES COMPLETE")
print("Output folder:", FIGURES)
