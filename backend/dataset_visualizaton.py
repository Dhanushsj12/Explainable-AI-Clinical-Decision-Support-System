import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


# ==========================================
# PATHS
# ==========================================

DATASET_PATH = "../datasets/cleaned/heart_cleaned.csv"
REPORT_FOLDER = "../reports"

os.makedirs(REPORT_FOLDER, exist_ok=True)


# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv(DATASET_PATH)

print("====================================")
print("HEART DISEASE DATASET")
print("====================================")

print("Dataset Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())


# ==========================================
# 1. HEART DISEASE CLASS DISTRIBUTION
# ==========================================

plt.figure(figsize=(7, 5))

sns.countplot(
    data=df,
    x="target"
)

plt.title("Heart Disease Class Distribution")
plt.xlabel("Heart Disease")
plt.ylabel("Number of Patients")

plt.xticks(
    [0, 1],
    ["No Heart Disease", "Heart Disease"]
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        REPORT_FOLDER,
        "heart_disease_distribution.png"
    ),
    dpi=300
)

plt.show()


# ==========================================
# 2. AGE DISTRIBUTION
# ==========================================

plt.figure(figsize=(8, 5))

sns.histplot(
    data=df,
    x="age",
    bins=15,
    kde=True
)

plt.title("Age Distribution of Patients")
plt.xlabel("Age")
plt.ylabel("Number of Patients")

plt.tight_layout()

plt.savefig(
    os.path.join(
        REPORT_FOLDER,
        "age_distribution.png"
    ),
    dpi=300
)

plt.show()


# ==========================================
# 3. AGE VS MAXIMUM HEART RATE
# ==========================================

plt.figure(figsize=(8, 5))

sns.scatterplot(
    data=df,
    x="age",
    y="thalach",
    hue="target"
)

plt.title("Age vs Maximum Heart Rate")
plt.xlabel("Age")
plt.ylabel("Maximum Heart Rate")

plt.legend(
    title="Heart Disease",
    labels=[
        "No Heart Disease",
        "Heart Disease"
    ]
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        REPORT_FOLDER,
        "age_vs_heart_rate.png"
    ),
    dpi=300
)

plt.show()


# ==========================================
# 4. CORRELATION HEATMAP
# ==========================================

plt.figure(figsize=(12, 9))

correlation = df.corr(numeric_only=True)

sns.heatmap(
    correlation,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    linewidths=0.5
)

plt.title(
    "Correlation Between Clinical Features"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        REPORT_FOLDER,
        "clinical_feature_correlation.png"
    ),
    dpi=300
)

plt.show()


# ==========================================
# DATASET SUMMARY
# ==========================================

print("\n====================================")
print("DATASET SUMMARY")
print("====================================")

print("Total Patients:", len(df))

print(
    "Total Columns:",
    len(df.columns)
)

if "target" in df.columns:

    print(
        "Heart Disease Cases:",
        int((df["target"] == 1).sum())
    )

    print(
        "No Heart Disease Cases:",
        int((df["target"] == 0).sum())
    )


print("\nMissing Values:")

print(
    df.isnull().sum()
)

print("\n====================================")
print("GRAPHS GENERATED SUCCESSFULLY")
print("====================================")