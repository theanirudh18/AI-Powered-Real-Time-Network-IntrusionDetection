"""
==========================================================
Project : AI-Powered Real-Time Network Intrusion Detection
Module  : Feature Selection
Author  : Anirudh Singh

Description:
    Performs feature selection on the cleaned dataset.

    Steps:
    - Fix Label Names
    - Remove Duplicate Rows
    - Remove Negative Flow Duration
    - Remove Constant Features
    - Remove Duplicate Columns
    - Remove Highly Correlated Features
    - Remove Low Variance Features
    - Save Reports
==========================================================
"""

from pathlib import Path
import json

import numpy as np
import pandas as pd
from sklearn.feature_selection import VarianceThreshold

# ==========================================================
# PATHS
# ==========================================================

INPUT_FILE = Path("dataset/interim/clean_dataset.csv")

OUTPUT_FILE = Path("dataset/interim/selected_dataset.csv")

METADATA_DIR = Path("dataset/metadata")

METADATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

SELECTED_FEATURES = (
    METADATA_DIR /
    "selected_features.json"
)

REMOVED_FEATURES = (
    METADATA_DIR /
    "removed_features.json"
)

REPORT_FILE = (
    METADATA_DIR /
    "feature_selection_report.txt"
)

# ==========================================================
# CONFIGURATION
# ==========================================================

CORRELATION_THRESHOLD = 0.95

VARIANCE_THRESHOLD = 0.0

LABEL_FIXES = {

    "Web Attack � Brute Force":
        "Web Attack - Brute Force",

    "Web Attack � XSS":
        "Web Attack - XSS",

    "Web Attack � Sql Injection":
        "Web Attack - Sql Injection",

}

# ==========================================================
# LOAD DATASET
# ==========================================================

def load_dataset():

    print("=" * 70)
    print("Loading Dataset...")
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
# REMOVE DUPLICATE ROWS
# ==========================================================

def remove_duplicate_rows(df):

    duplicates = df.duplicated().sum()

    if duplicates > 0:

        df = df.drop_duplicates()

    print(f"Duplicate Rows Removed : {duplicates:,}")

    return df, duplicates

# ==========================================================
# REMOVE NEGATIVE FLOW DURATION
# ==========================================================

def remove_negative_flow_duration(df):

    removed = 0

    if "Flow Duration" in df.columns:

        removed = (
            df["Flow Duration"] < 0
        ).sum()

        df = df[
            df["Flow Duration"] >= 0
        ]

    print(
        f"Negative Flow Duration Removed : {removed}"
    )

    return df, removed

# ==========================================================
# REMOVE CONSTANT FEATURES
# ==========================================================

def remove_constant_features(df):

    constant_features = []

    for column in df.columns:

        if column == "Label":
            continue

        if df[column].nunique(
            dropna=False
        ) <= 1:

            constant_features.append(column)

    df.drop(
        columns=constant_features,
        inplace=True
    )

    print(
        f"Constant Features Removed : {len(constant_features)}"
    )

    return df, constant_features

# ==========================================================
# REMOVE DUPLICATE COLUMNS
# ==========================================================

def remove_duplicate_columns(df):

    duplicate_columns = []

    columns = df.columns

    for i in range(len(columns)):

        for j in range(i + 1, len(columns)):

            if columns[j] == "Label":
                continue

            if df[columns[i]].equals(
                df[columns[j]]
            ):

                duplicate_columns.append(
                    columns[j]
                )

    duplicate_columns = list(
        set(duplicate_columns)
    )

    df.drop(
        columns=duplicate_columns,
        inplace=True
    )

    print(
        f"Duplicate Features Removed : {len(duplicate_columns)}"
    )

    return df, duplicate_columns

    # ==========================================================
# REMOVE HIGHLY CORRELATED FEATURES
# ==========================================================

def remove_correlated_features(df):

    numeric_df = df.select_dtypes(include=[np.number])

    corr_matrix = numeric_df.corr().abs()

    upper = corr_matrix.where(
        np.triu(
            np.ones(corr_matrix.shape),
            k=1
        ).astype(bool)
    )

    correlated_features = [

        column

        for column in upper.columns

        if any(
            upper[column] > CORRELATION_THRESHOLD
        )

    ]

    df.drop(
        columns=correlated_features,
        inplace=True
    )

    print(
        f"Highly Correlated Features Removed : {len(correlated_features)}"
    )

    return df, correlated_features


# ==========================================================
# REMOVE LOW VARIANCE FEATURES
# ==========================================================

def remove_low_variance_features(df):

    feature_columns = [

        column

        for column in df.columns

        if column != "Label"

    ]

    selector = VarianceThreshold(
        threshold=VARIANCE_THRESHOLD
    )

    selector.fit(
        df[feature_columns]
    )

    selected_mask = selector.get_support()

    selected = [
        column

        for column, keep

        in zip(
            feature_columns,
            selected_mask
        )

        if keep
    ]

    removed = list(
        set(feature_columns) -
        set(selected)
    )

    final_df = df[selected].copy()

    final_df["Label"] = df["Label"]

    print(
        f"Low Variance Features Removed : {len(removed)}"
    )

    return final_df, removed


# ==========================================================
# SAVE SELECTED FEATURES
# ==========================================================

def save_selected_features(df):

    features = [

        column

        for column in df.columns

        if column != "Label"

    ]

    with open(
        SELECTED_FEATURES,
        "w"
    ) as file:

        json.dump(

            {

                "total_features": len(features),

                "feature_order": features

            },

            file,

            indent=4

        )

    print("Selected Features Saved")


# ==========================================================
# SAVE REMOVED FEATURES
# ==========================================================

def save_removed_features(

    constant,

    duplicate,

    correlated,

    variance

):

    report = {

        "constant_features": constant,

        "duplicate_features": duplicate,

        "correlated_features": correlated,

        "low_variance_features": variance

    }

    with open(

        REMOVED_FEATURES,

        "w"

    ) as file:

        json.dump(

            report,

            file,

            indent=4

        )

    print("Removed Features Saved")
    # ==========================================================
# SAVE REPORT
# ==========================================================

def save_report(
    original_shape,
    final_shape,
    duplicate_rows,
    negative_rows,
    constant_features,
    duplicate_features,
    correlated_features,
    low_variance_features,
):

    with open(REPORT_FILE, "w") as file:

        file.write("=" * 70 + "\n")
        file.write("FEATURE SELECTION REPORT\n")
        file.write("=" * 70 + "\n\n")

        file.write(f"Original Rows    : {original_shape[0]:,}\n")
        file.write(f"Final Rows       : {final_shape[0]:,}\n\n")

        file.write(f"Original Columns : {original_shape[1]}\n")
        file.write(f"Final Columns    : {final_shape[1]}\n")
        file.write(f"Selected Features: {final_shape[1]-1}\n\n")

        file.write(f"Duplicate Rows Removed        : {duplicate_rows}\n")
        file.write(f"Negative Flow Duration Removed: {negative_rows}\n")
        file.write(f"Constant Features Removed     : {len(constant_features)}\n")
        file.write(f"Duplicate Features Removed    : {len(duplicate_features)}\n")
        file.write(f"Correlated Features Removed   : {len(correlated_features)}\n")
        file.write(f"Low Variance Features Removed : {len(low_variance_features)}\n")


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 70)
    print("STARTING FEATURE SELECTION")
    print("=" * 70)

    df = load_dataset()

    original_shape = df.shape

    # Duplicate Rows
    df, duplicate_rows = remove_duplicate_rows(df)

    # Negative Flow Duration
    df, negative_rows = remove_negative_flow_duration(df)

    # Constant Features
    df, constant_features = remove_constant_features(df)

    # Duplicate Columns
    df, duplicate_features = remove_duplicate_columns(df)

    # Correlated Features
    df, correlated_features = remove_correlated_features(df)

    # Low Variance Features
    df, low_variance_features = remove_low_variance_features(df)

    final_shape = df.shape

    # Save Dataset
    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # Save Metadata
    save_selected_features(df)

    save_removed_features(
        constant_features,
        duplicate_features,
        correlated_features,
        low_variance_features
    )

    save_report(
        original_shape,
        final_shape,
        duplicate_rows,
        negative_rows,
        constant_features,
        duplicate_features,
        correlated_features,
        low_variance_features
    )

    print("\n" + "=" * 70)
    print("FEATURE SELECTION COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print(f"\nFinal Dataset Shape : {df.shape}")

    print(f"\nDataset Saved : {OUTPUT_FILE}")
    print(f"Selected Features : {SELECTED_FEATURES}")
    print(f"Removed Features : {REMOVED_FEATURES}")
    print(f"Report : {REPORT_FILE}")


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    main()