
"""
06_inspect_final_tables.py

Inspects the seven final CSV tables without running any model code.
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "research" / "results"

FILES = [
    "model_performance_final.csv",
    "agreement_final.csv",
    "counterfactual_final.csv",
    "stability_statistics_final.csv",
    "augmentation_heart_final.csv",
    "baseline_available_final.csv",
    "ablation_posthoc_final.csv",
]

print("=" * 72)
print("XAI-CDSS FINAL TABLE INSPECTION")
print("=" * 72)

for name in FILES:
    path = RESULTS / name
    print(f"\n--- {name} ---")
    if not path.exists():
        print("MISSING")
        continue
    df = pd.read_csv(path)
    print("Rows:", len(df))
    print("Columns:", ", ".join(df.columns.astype(str)))
    print(df.to_string(index=False))
