from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]

DISEASES = {
    "diabetes": {
        "processed_dir": PROJECT_ROOT / "datasets" / "processed" / "diabetes",
        "target_column": "class",
        "categorical_like": [
            "Gender",
            "Polyuria",
            "Polydipsia",
            "sudden weight loss",
            "weakness",
            "Polyphagia",
            "Genital thrush",
            "visual blurring",
            "Itching",
            "Irritability",
            "delayed healing",
            "partial paresis",
            "muscle stiffness",
            "Alopecia",
            "Obesity",
            "class",
        ],
    },
    "ckd": {
        "processed_dir": PROJECT_ROOT / "datasets" / "processed" / "ckd",
        "target_column": "class",
        "categorical_like": [
            "rbc",
            "pc",
            "pcc",
            "ba",
            "htn",
            "dm",
            "cad",
            "appet",
            "pe",
            "ane",
            "class",
        ],
    },
    "stroke": {
        "processed_dir": PROJECT_ROOT / "datasets" / "processed" / "stroke",
        "target_column": "stroke",
        "categorical_like": [
            "gender",
            "hypertension",
            "heart_disease",
            "ever_married",
            "work_type",
            "Residence_type",
            "smoking_status",
            "stroke",
        ],
    },
}


def load_split(config):
    processed_dir = config["processed_dir"]

    x_train = pd.read_csv(processed_dir / "x_train.csv")
    y_train = pd.read_csv(processed_dir / "y_train.csv")
    x_test = pd.read_csv(processed_dir / "x_test.csv")
    y_test = pd.read_csv(processed_dir / "y_test.csv")

    target_column = config["target_column"]

    train = x_train.copy()
    train[target_column] = y_train.iloc[:, 0].astype(int)

    test = x_test.copy()
    test[target_column] = y_test.iloc[:, 0].astype(int)

    return train, test


def sample_with_sdv(train, target_column, rows):
    from sdv.metadata import SingleTableMetadata
    from sdv.single_table import GaussianCopulaSynthesizer

    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(data=train)
    metadata.update_column(
        column_name=target_column,
        sdtype="categorical",
    )

    synthesizer = GaussianCopulaSynthesizer(metadata=metadata)
    synthesizer.fit(train)

    return synthesizer.sample(num_rows=rows)


def sample_with_bootstrap(train, config, rows, random_state=42):
    rng = np.random.default_rng(random_state)
    synthetic = train.sample(
        n=rows,
        replace=True,
        random_state=random_state,
    ).reset_index(drop=True)

    categorical_like = set(config["categorical_like"])

    for column in synthetic.columns:
        if column in categorical_like:
            continue

        values = train[column].dropna()
        if values.empty:
            continue

        noise = rng.normal(
            loc=0,
            scale=max(float(values.std()) * 0.035, 1e-6),
            size=rows,
        )

        synthetic[column] = synthetic[column].astype(float) + noise
        synthetic[column] = synthetic[column].clip(
            lower=float(values.min()),
            upper=float(values.max()),
        )

    return synthetic


def clean_synthetic(synthetic, train, config):
    target_column = config["target_column"]
    categorical_like = set(config["categorical_like"])

    for column in synthetic.columns:
        if column in categorical_like:
            allowed_values = sorted(
                train[column]
                .dropna()
                .unique()
                .tolist()
            )

            if not allowed_values:
                continue

            synthetic[column] = pd.to_numeric(
                synthetic[column],
                errors="coerce",
            )
            synthetic[column] = synthetic[column].round()
            synthetic[column] = synthetic[column].fillna(
                train[column].mode().iloc[0]
            )
            synthetic[column] = synthetic[column].apply(
                lambda value: min(
                    allowed_values,
                    key=lambda allowed: abs(float(allowed) - float(value)),
                )
            )

        else:
            synthetic[column] = pd.to_numeric(
                synthetic[column],
                errors="coerce",
            )
            synthetic[column] = synthetic[column].fillna(
                train[column].median()
            )
            synthetic[column] = synthetic[column].clip(
                lower=train[column].min(),
                upper=train[column].max(),
            )

    synthetic[target_column] = synthetic[target_column].astype(int)
    return synthetic[train.columns].reset_index(drop=True)


def validate(real, synthetic, target_column):
    real_numeric = real.select_dtypes(include=np.number)
    synthetic_numeric = synthetic.select_dtypes(include=np.number)
    common_columns = [
        column
        for column in real_numeric.columns
        if column in synthetic_numeric.columns
    ]

    if common_columns:
        correlation_difference = (
            real_numeric[common_columns].corr()
            - synthetic_numeric[common_columns].corr()
        ).abs()
        average_correlation_difference = float(
            np.nan_to_num(correlation_difference.values).mean()
        )
    else:
        average_correlation_difference = 0.0

    return {
        "real_train_rows": len(real),
        "synthetic_rows": len(synthetic),
        "augmented_rows": len(real) + len(synthetic),
        "columns": len(synthetic.columns),
        "missing_values": int(synthetic.isnull().sum().sum()),
        "exact_duplicates": int(synthetic.duplicated().sum()),
        "target_values": ",".join(
            str(value)
            for value in sorted(synthetic[target_column].unique().tolist())
        ),
        "average_correlation_difference": round(
            average_correlation_difference,
            4,
        ),
    }


def augment_disease(disease, rows=50000):
    config = DISEASES[disease]
    target_column = config["target_column"]
    output_dir = PROJECT_ROOT / "datasets" / "augmented" / disease
    output_dir.mkdir(parents=True, exist_ok=True)

    train, test = load_split(config)

    real_train_file = output_dir / f"{disease}_train_real.csv"
    real_test_file = output_dir / f"{disease}_test_real.csv"
    synthetic_file = output_dir / f"{disease}_train_synthetic.csv"
    augmented_file = output_dir / f"{disease}_train_augmented.csv"
    summary_file = output_dir / f"{disease}_synthetic_validation_summary.csv"

    train.to_csv(real_train_file, index=False)
    test.to_csv(real_test_file, index=False)

    try:
        synthetic = sample_with_sdv(
            train=train,
            target_column=target_column,
            rows=rows,
        )
        method = "SDV Gaussian Copula"
    except Exception as error:
        print(f"{disease}: SDV unavailable or failed: {error!r}")
        synthetic = sample_with_bootstrap(
            train=train,
            config=config,
            rows=rows,
        )
        method = "bootstrap with numeric jitter fallback"

    synthetic = clean_synthetic(
        synthetic=synthetic,
        train=train,
        config=config,
    )

    augmented = pd.concat(
        [train, synthetic],
        ignore_index=True,
    )

    synthetic.to_csv(synthetic_file, index=False)
    augmented.to_csv(augmented_file, index=False)

    summary = validate(
        real=train,
        synthetic=synthetic,
        target_column=target_column,
    )
    summary["method"] = method

    pd.DataFrame([summary]).to_csv(summary_file, index=False)

    print()
    print("=" * 60)
    print(f"{disease.upper()} AUGMENTATION COMPLETE")
    print("=" * 60)
    print("Method:", method)
    print("Real training rows:", len(train))
    print("Real testing rows:", len(test))
    print("Synthetic rows:", len(synthetic))
    print("Final augmented rows:", len(augmented))
    print("Target distribution:")
    print(augmented[target_column].value_counts().sort_index())
    print("Saved:", synthetic_file)
    print("Saved:", augmented_file)
    print("Saved:", summary_file)


def main():
    for disease in ["diabetes", "ckd", "stroke"]:
        augment_disease(disease)


if __name__ == "__main__":
    main()
