import pandas as pd
from sdv.metadata import SingleTableMetadata
from sdv.single_table import GaussianCopulaSynthesizer

# ============================================================
# PATHS
# ============================================================

TRAIN_FILE = "datasets/augmented/heart/heart_train_real.csv"

SYNTHETIC_FILE = "datasets/augmented/heart/heart_train_synthetic.csv"

AUGMENTED_FILE = "datasets/augmented/heart/heart_train_augmented.csv"


# ============================================================
# LOAD REAL TRAINING DATA
# ============================================================

train_real = pd.read_csv(TRAIN_FILE)

print("\nREAL TRAINING DATA")
print("------------------")
print("Rows:", len(train_real))
print("Columns:", len(train_real.columns))

print("\nOriginal target distribution:")
print(train_real["target"].value_counts().sort_index())


# ============================================================
# CONVERT HEART TARGET TO BINARY
# ============================================================
# Original UCI-style target:
#
# 0 = No disease
# 1,2,3,4 = Disease
#
# Project model uses:
# 0 = No Heart Disease
# 1 = Heart Disease
#
# IMPORTANT:
# This conversion is ONLY for the separate augmentation
# dataset. Existing processed train/test files are untouched.
# ============================================================

train_real["target"] = (
    train_real["target"] > 0
).astype(int)


print("\nBinary target distribution:")
print(train_real["target"].value_counts().sort_index())


# ============================================================
# SDV METADATA
# ============================================================

metadata = SingleTableMetadata()

metadata.detect_from_dataframe(
    data=train_real
)


# ============================================================
# TARGET AS CATEGORICAL
# ============================================================

metadata.update_column(
    column_name="target",
    sdtype="categorical"
)


# ============================================================
# CREATE GAUSSIAN COPULA SYNTHESIZER
# ============================================================

print("\nCreating Gaussian Copula synthesizer...")

synthesizer = GaussianCopulaSynthesizer(
    metadata=metadata
)


# ============================================================
# FIT ONLY ON REAL TRAINING DATA
# ============================================================

print("Fitting synthesizer on REAL TRAINING DATA only...")

synthesizer.fit(train_real)


# ============================================================
# GENERATE 50,000 SYNTHETIC ROWS
# ============================================================

print("\nGenerating 50,000 synthetic rows...")

synthetic_data = synthesizer.sample(
    num_rows=50000
)


# ============================================================
# ENSURE TARGET IS INTEGER
# ============================================================

synthetic_data["target"] = (
    pd.to_numeric(
        synthetic_data["target"],
        errors="coerce"
    )
    .round()
    .astype(int)
)


# ============================================================
# SAFETY CHECK
# ============================================================

synthetic_data = synthetic_data[
    synthetic_data["target"].isin([0, 1])
].reset_index(drop=True)


# ============================================================
# SAVE SYNTHETIC DATA
# ============================================================

synthetic_data.to_csv(
    SYNTHETIC_FILE,
    index=False
)


# ============================================================
# CREATE AUGMENTED TRAINING DATA
# ============================================================

augmented_data = pd.concat(
    [
        train_real,
        synthetic_data
    ],
    ignore_index=True
)


augmented_data.to_csv(
    AUGMENTED_FILE,
    index=False
)


# ============================================================
# RESULTS
# ============================================================

print("\nGENERATION COMPLETE")
print("===================")

print("\nReal training rows:")
print(len(train_real))

print("\nSynthetic rows:")
print(len(synthetic_data))

print("\nFinal augmented training rows:")
print(len(augmented_data))


print("\nReal target distribution:")
print(
    train_real["target"]
    .value_counts()
    .sort_index()
)


print("\nSynthetic target distribution:")
print(
    synthetic_data["target"]
    .value_counts()
    .sort_index()
)


print("\nAugmented target distribution:")
print(
    augmented_data["target"]
    .value_counts()
    .sort_index()
)


print("\nSaved:")
print(SYNTHETIC_FILE)
print(AUGMENTED_FILE)