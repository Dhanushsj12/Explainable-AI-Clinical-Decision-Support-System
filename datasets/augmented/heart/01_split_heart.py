import pandas as pd
import os


# ============================================================
# PATHS
# ============================================================

X_TRAIN_FILE = "datasets/processed/x_train.csv"
Y_TRAIN_FILE = "datasets/processed/y_train.csv"

X_TEST_FILE = "datasets/processed/x_test.csv"
Y_TEST_FILE = "datasets/processed/y_test.csv"

OUTPUT_DIR = "datasets/augmented/heart"

TRAIN_FILE = os.path.join(
    OUTPUT_DIR,
    "heart_train_real.csv"
)

TEST_FILE = os.path.join(
    OUTPUT_DIR,
    "heart_test_real.csv"
)


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# LOAD EXISTING PROCESSED DATA
# ============================================================

x_train = pd.read_csv(X_TRAIN_FILE)
y_train = pd.read_csv(Y_TRAIN_FILE)

x_test = pd.read_csv(X_TEST_FILE)
y_test = pd.read_csv(Y_TEST_FILE)


# ============================================================
# COMBINE X + Y
# ============================================================

train_real = x_train.copy()
train_real["target"] = y_train["target"]

test_real = x_test.copy()
test_real["target"] = y_test["target"]


# ============================================================
# ADD SOURCE TAG
# ============================================================

train_real["data_source"] = "original"
test_real["data_source"] = "original"


# ============================================================
# INFORMATION
# ============================================================

print("\n==========================================")
print("HEART AUGMENTATION DATA PREPARATION")
print("==========================================")

print("\nREAL TRAINING DATA")
print("------------------")
print("Rows:", len(train_real))
print("Target distribution:")
print(
    train_real["target"]
    .value_counts()
    .sort_index()
)

print("\nREAL TESTING DATA")
print("-----------------")
print("Rows:", len(test_real))
print("Target distribution:")
print(
    test_real["target"]
    .value_counts()
    .sort_index()
)


# ============================================================
# SAVE
# ============================================================

train_real.to_csv(
    TRAIN_FILE,
    index=False
)

test_real.to_csv(
    TEST_FILE,
    index=False
)


print("\nSaved:")
print(TRAIN_FILE)
print(TEST_FILE)

print("\nIMPORTANT:")
print("Existing processed train/test files were NOT modified.")
print("Test data remains completely real and untouched.")