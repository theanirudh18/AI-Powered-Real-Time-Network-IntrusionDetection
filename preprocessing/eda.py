"""
==========================================================
Project : AI-Powered Real-Time Network Intrusion Detection
Module  : Exploratory Data Analysis (EDA)
Author  : Anirudh Singh
Description:
    Performs Exploratory Data Analysis (EDA) on the cleaned
    CICIDS2017 dataset.

    Outputs:
        - Dataset Summary
        - Data Types
        - Missing Values
        - Class Distribution
        - Statistical Summary
        - Correlation Heatmap
        - Histograms
        - Boxplots
==========================================================
"""

from pathlib import Path
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

warnings.filterwarnings("ignore")

# ==========================================================
# PATHS
# ==========================================================

INPUT_FILE = Path("dataset/interim/clean_dataset.csv")

GRAPH_DIR = Path("graphs/eda")
REPORT_DIR = Path("reports/eda")

GRAPH_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================================
# CONFIGURATION
# ==========================================================

SAMPLE_SIZE = 50000
RANDOM_STATE = 42

LABEL_FIXES = {
    "Web Attack � Brute Force": "Web Attack - Brute Force",
    "Web Attack � XSS": "Web Attack - XSS",
    "Web Attack � Sql Injection": "Web Attack - Sql Injection",
}

# ==========================================================
# LOAD DATASET
# ==========================================================

def load_dataset():

    print("=" * 70)
    print("Loading Clean Dataset...")
    print("=" * 70)

    df = pd.read_csv(
        INPUT_FILE,
        low_memory=False
    )

    df.columns = df.columns.str.strip()

    df["Label"] = (
        df["Label"]
        .astype(str)
        .str.strip()
        .replace(LABEL_FIXES)
    )

    print(f"Dataset Shape : {df.shape}")

    return df

# ==========================================================
# SAVE DATASET SUMMARY
# ==========================================================

def dataset_summary(df):

    summary_path = REPORT_DIR / "dataset_summary.txt"

    with open(summary_path, "w") as file:

        file.write("=" * 60 + "\n")
        file.write("DATASET SUMMARY\n")
        file.write("=" * 60 + "\n\n")

        file.write(f"Rows : {df.shape[0]}\n")
        file.write(f"Columns : {df.shape[1]}\n\n")

        file.write(f"Numeric Features : {len(df.select_dtypes(include=np.number).columns)}\n")
        file.write(f"Categorical Features : {len(df.select_dtypes(exclude=np.number).columns)}\n\n")

        file.write("Columns\n")
        file.write("-" * 50 + "\n")

        for column in df.columns:
            file.write(column + "\n")

    print("✔ Dataset Summary Saved")

# ==========================================================
# DATA TYPES
# ==========================================================

def save_data_types(df):

    data_types = pd.DataFrame({
        "Feature": df.columns,
        "Data Type": df.dtypes.astype(str)
    })

    data_types.to_csv(
        REPORT_DIR / "data_types.csv",
        index=False
    )

    print("✔ Data Types Saved")

# ==========================================================
# MISSING VALUES
# ==========================================================

def missing_value_report(df):

    missing = pd.DataFrame({
        "Feature": df.columns,
        "Missing Values": df.isnull().sum(),
        "Percentage": (
            df.isnull().sum() /
            len(df)
        ) * 100
    })

    missing.to_csv(
        REPORT_DIR / "missing_values.csv",
        index=False
    )

    total_missing = missing["Missing Values"].sum()

    print(f"✔ Missing Values Report Saved ({total_missing} Missing Values)")

# ==========================================================
# STATISTICAL SUMMARY
# ==========================================================

def statistical_summary(df):

    summary = df.describe(include="all").transpose()

    summary.to_csv(
        REPORT_DIR / "feature_statistics.csv"
    )

    print("✔ Statistical Summary Saved")

# ==========================================================
# CLASS DISTRIBUTION
# ==========================================================

def class_distribution(df):

    class_df = (
        df["Label"]
        .value_counts()
        .reset_index()
    )

    class_df.columns = [
        "Class",
        "Count"
    ]

    class_df.to_csv(
        REPORT_DIR / "class_distribution.csv",
        index=False
    )

    plt.figure(figsize=(12,7))

    sns.barplot(
        data=class_df,
        y="Class",
        x="Count"
    )

    plt.title("Attack Class Distribution")

    plt.tight_layout()

    plt.savefig(
        GRAPH_DIR / "class_distribution.png",
        dpi=300
    )

    plt.close()

    print("✔ Class Distribution Saved")

    # ==========================================================
# SAMPLE DATA FOR VISUALIZATION
# ==========================================================

def get_sample(df):

    if len(df) > SAMPLE_SIZE:
        sample_df = df.sample(
            n=SAMPLE_SIZE,
            random_state=RANDOM_STATE
        )
    else:
        sample_df = df.copy()

    print(f"✔ Using {len(sample_df):,} rows for visualization")

    return sample_df

# ==========================================================
# CORRELATION HEATMAP
# ==========================================================

def correlation_heatmap(sample_df):

    numeric_df = sample_df.select_dtypes(include=np.number)

    plt.figure(figsize=(20,18))

    correlation = numeric_df.corr()

    sns.heatmap(
        correlation,
        cmap="coolwarm",
        center=0,
        square=False,
        cbar=True
    )

    plt.title("Feature Correlation Heatmap")

    plt.tight_layout()

    plt.savefig(
        GRAPH_DIR / "correlation_heatmap.png",
        dpi=300
    )

    plt.close()

    print("✔ Correlation Heatmap Saved")

# ==========================================================
# FEATURE HISTOGRAMS
# ==========================================================

def feature_histograms(sample_df):

    numeric_columns = sample_df.select_dtypes(
        include=np.number
    ).columns

    columns = numeric_columns[:12]

    fig, axes = plt.subplots(
        3,
        4,
        figsize=(20,14)
    )

    axes = axes.flatten()

    for i, column in enumerate(columns):

        sns.histplot(
            sample_df[column],
            bins=50,
            kde=False,
            ax=axes[i]
        )

        axes[i].set_title(column, fontsize=9)

    plt.tight_layout()

    plt.savefig(
        GRAPH_DIR / "feature_histograms.png",
        dpi=300
    )

    plt.close()

    print("✔ Feature Histograms Saved")

# ==========================================================
# BOXPLOTS
# ==========================================================

def feature_boxplots(sample_df):

    numeric_columns = sample_df.select_dtypes(
        include=np.number
    ).columns

    columns = numeric_columns[:12]

    fig, axes = plt.subplots(
        3,
        4,
        figsize=(20,14)
    )

    axes = axes.flatten()

    for i, column in enumerate(columns):

        sns.boxplot(
            x=sample_df[column],
            ax=axes[i]
        )

        axes[i].set_title(column, fontsize=9)

    plt.tight_layout()

    plt.savefig(
        GRAPH_DIR / "feature_boxplots.png",
        dpi=300
    )

    plt.close()

    print("✔ Feature Boxplots Saved")

# ==========================================================
# NEGATIVE VALUE REPORT
# ==========================================================

def negative_value_report(df):

    report = []

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns

    for column in numeric_columns:

        negatives = (df[column] < 0).sum()

        if negatives > 0:

            report.append(
                {
                    "Feature": column,
                    "Negative Values": negatives
                }
            )

    report_df = pd.DataFrame(report)

    report_df.to_csv(
        REPORT_DIR / "negative_values.csv",
        index=False
    )

    print("✔ Negative Value Report Saved")

# ==========================================================
# CONSTANT FEATURE REPORT
# ==========================================================

def constant_feature_report(df):

    constant = []

    for column in df.columns:

        if column == "Label":
            continue

        if df[column].nunique(dropna=False) <= 1:

            constant.append(column)

    constant_df = pd.DataFrame(
        {
            "Constant Features": constant
        }
    )

    constant_df.to_csv(
        REPORT_DIR / "constant_features.csv",
        index=False
    )

    print(f"✔ Constant Feature Report Saved ({len(constant)} features)")

# ==========================================================
# INVALID LABEL REPORT
# ==========================================================

def invalid_label_report(df):

    labels = sorted(df["Label"].unique())

    pd.DataFrame(
        {
            "Labels": labels
        }
    ).to_csv(
        REPORT_DIR / "labels.csv",
        index=False
    )

    print("✔ Label Report Saved")

    # ==========================================================
# FINAL EDA REPORT
# ==========================================================

def generate_report(df):

    report_path = REPORT_DIR / "eda_report.txt"

    numeric_features = len(
        df.select_dtypes(include=np.number).columns
    )

    categorical_features = len(
        df.select_dtypes(exclude=np.number).columns
    )

    duplicate_rows = df.duplicated().sum()

    negative_flow_duration = 0

    if "Flow Duration" in df.columns:
        negative_flow_duration = (
            df["Flow Duration"] < 0
        ).sum()

    class_distribution = (
        df["Label"]
        .value_counts()
    )

    with open(report_path, "w") as file:

        file.write("=" * 70 + "\n")
        file.write("EXPLORATORY DATA ANALYSIS REPORT\n")
        file.write("=" * 70 + "\n\n")

        file.write(f"Rows : {df.shape[0]:,}\n")
        file.write(f"Columns : {df.shape[1]}\n\n")

        file.write(f"Numeric Features : {numeric_features}\n")
        file.write(f"Categorical Features : {categorical_features}\n\n")

        file.write(f"Duplicate Rows : {duplicate_rows}\n")
        file.write(f"Negative Flow Duration : {negative_flow_duration}\n")
        file.write(f"Missing Values : {df.isnull().sum().sum()}\n\n")

        file.write("=" * 50 + "\n")
        file.write("CLASS DISTRIBUTION\n")
        file.write("=" * 50 + "\n\n")

        for label, count in class_distribution.items():
            file.write(f"{label:<35} {count:,}\n")

    print("✔ EDA Report Saved")


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("\n" + "=" * 70)
    print("STARTING EXPLORATORY DATA ANALYSIS")
    print("=" * 70 + "\n")

    df = load_dataset()

    sample_df = get_sample(df)

    dataset_summary(df)

    save_data_types(df)

    missing_value_report(df)

    statistical_summary(df)

    class_distribution(df)

    correlation_heatmap(sample_df)

    feature_histograms(sample_df)

    feature_boxplots(sample_df)

    negative_value_report(df)

    constant_feature_report(df)

    invalid_label_report(df)

    generate_report(df)

    print("\n" + "=" * 70)
    print("EDA COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print("\nGenerated Reports")

    print("------------------------------")

    print(f"Reports : {REPORT_DIR}")

    print(f"Graphs  : {GRAPH_DIR}")

    print("\nFiles Generated")

    print("------------------------------")

    print("dataset_summary.txt")

    print("eda_report.txt")

    print("class_distribution.csv")

    print("feature_statistics.csv")

    print("data_types.csv")

    print("missing_values.csv")

    print("negative_values.csv")

    print("constant_features.csv")

    print("labels.csv")

    print()

    print("class_distribution.png")

    print("correlation_heatmap.png")

    print("feature_histograms.png")

    print("feature_boxplots.png")

    print()


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":

    main()