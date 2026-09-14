import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE = Path("datasets/augmented/heart")

REAL_TRAIN_FILE = BASE / "heart_train_real.csv"
SYNTHETIC_FILE = BASE / "heart_train_synthetic.csv"


# ============================================================
# LOAD DATA
# ============================================================

real = pd.read_csv(REAL_TRAIN_FILE)
synthetic = pd.read_csv(SYNTHETIC_FILE)


print("\n==========================================")
print("HEART SYNTHETIC DATA VALIDATION")
print("==========================================")


# ============================================================
# BASIC INFORMATION
# ============================================================

print("\nREAL TRAINING DATA")
print("------------------")
print("Rows:", len(real))
print("Columns:", len(real.columns))

print("\nSYNTHETIC DATA")
print("--------------")
print("Rows:", len(synthetic))
print("Columns:", len(synthetic.columns))


# ============================================================
# 1. COLUMN CHECK
# ============================================================

print("\n1. COLUMN CHECK")
print("---------------")

real_columns = [
    c for c in real.columns
    if c != "data_source"
]

synthetic_columns = [
    c for c in synthetic.columns
    if c != "data_source"
]

if real_columns == synthetic_columns:
    print("PASS: Columns match")
else:
    print("WARNING: Columns do not match")

print("\nColumns:")
print(synthetic_columns)


# ============================================================
# 2. MISSING VALUES
# ============================================================

print("\n2. MISSING VALUE CHECK")
print("----------------------")

missing = synthetic.isnull().sum()

if missing.sum() == 0:
    print("PASS: No missing values")
else:
    print("WARNING: Missing values found")
    print(missing[missing > 0])


# ============================================================
# 3. DUPLICATE CHECK
# ============================================================

print("\n3. DUPLICATE CHECK")
print("------------------")

duplicates = synthetic.duplicated().sum()

print("Exact duplicate rows:", duplicates)

if duplicates == 0:
    print("PASS: No exact duplicates")
else:
    print("WARNING: Exact duplicates found")


# ============================================================
# 4. CLINICAL RANGE CHECK
# ============================================================

print("\n4. CLINICAL RANGE CHECK")
print("-----------------------")

ranges = {
    "age": (0, 120),
    "trestbps": (50, 250),
    "chol": (50, 700),
    "thalach": (50, 250),
    "oldpeak": (0, 10),
    "ca": (0, 3),
    "cp": (1, 4),
    "restecg": (0, 2),
    "slope": (1, 3),
    "thal": (0, 7),
    "sex": (0, 1),
    "fbs": (0, 1),
    "exang": (0, 1),
    "target": (0, 4)
}

range_failed = False

for column, (minimum, maximum) in ranges.items():

    if column not in synthetic.columns:
        continue

    values = synthetic[column]

    invalid = (
        (values < minimum) |
        (values > maximum)
    ).sum()

    print(
        f"{column:10} "
        f"min={values.min():.2f} "
        f"max={values.max():.2f} "
        f"invalid={invalid}"
    )

    if invalid > 0:
        range_failed = True

if not range_failed:
    print("\nPASS: No obvious out-of-range values")
else:
    print("\nWARNING: Some values are outside expected ranges")


# ============================================================
# 5. CATEGORICAL VALUE CHECK
# ============================================================

print("\n5. CATEGORICAL VALUE CHECK")
print("--------------------------")

categorical_columns = [
    "sex",
    "cp",
    "fbs",
    "restecg",
    "exang",
    "slope",
    "ca",
    "thal",
    "target"
]

for column in categorical_columns:

    if column in synthetic.columns:

        values = sorted(
            synthetic[column]
            .dropna()
            .unique()
            .tolist()
        )

        print(f"{column:10}: {values}")


# ============================================================
# 6. TARGET DISTRIBUTION
# ============================================================

print("\n6. TARGET DISTRIBUTION")
print("----------------------")

real_target = (
    real["target"]
    .value_counts()
    .sort_index()
)

synthetic_target = (
    synthetic["target"]
    .value_counts()
    .sort_index()
)

target_table = pd.DataFrame({
    "Real Train": real_target,
    "Synthetic": synthetic_target
}).fillna(0)

target_table["Real %"] = (
    target_table["Real Train"] /
    target_table["Real Train"].sum() * 100
).round(2)

target_table["Synthetic %"] = (
    target_table["Synthetic"] /
    target_table["Synthetic"].sum() * 100
).round(2)

print(target_table)


# ============================================================
# 7. REAL VS SYNTHETIC STATISTICS
# ============================================================

print("\n7. REAL VS SYNTHETIC STATISTICS")
print("--------------------------------")

numeric_columns = [
    "age",
    "trestbps",
    "chol",
    "thalach",
    "oldpeak"
]

for column in numeric_columns:

    if column not in real.columns:
        continue

    print(f"\n{column}")

    print(
        "Real      :",
        "mean =", round(real[column].mean(), 2),
        "std =", round(real[column].std(), 2),
        "min =", round(real[column].min(), 2),
        "max =", round(real[column].max(), 2)
    )

    print(
        "Synthetic :",
        "mean =", round(synthetic[column].mean(), 2),
        "std =", round(synthetic[column].std(), 2),
        "min =", round(synthetic[column].min(), 2),
        "max =", round(synthetic[column].max(), 2)
    )


# ============================================================
# 8. CORRELATION CHECK
# ============================================================

print("\n8. CORRELATION CHECK")
print("--------------------")

real_numeric = real.select_dtypes(include=np.number)
synthetic_numeric = synthetic.select_dtypes(include=np.number)

real_corr = real_numeric.corr()
synthetic_corr = synthetic_numeric.corr()

common_columns = [
    column
    for column in real_corr.columns
    if column in synthetic_corr.columns
]

correlation_difference = (
    real_corr.loc[common_columns, common_columns]
    -
    synthetic_corr.loc[common_columns, common_columns]
).abs()

average_difference = correlation_difference.values.mean()

print(
    "Average absolute correlation difference:",
    round(average_difference, 4)
)


# ============================================================
# 9. SAVE VALIDATION SUMMARY
# ============================================================

summary = {
    "real_train_rows": len(real),
    "synthetic_rows": len(synthetic),
    "columns": len(synthetic.columns),
    "missing_values": int(
        synthetic.isnull().sum().sum()
    ),
    "exact_duplicates": int(duplicates),
    "average_correlation_difference":
        round(average_difference, 4)
}

summary_df = pd.DataFrame([summary])

output_file = (
    BASE /
    "heart_synthetic_validation_summary.csv"
)

summary_df.to_csv(
    output_file,
    index=False
)


# ============================================================
# COMPLETE
# ============================================================

print("\n==========================================")
print("VALIDATION COMPLETE")
print("==========================================")

print("\nSaved:")
print(output_file)