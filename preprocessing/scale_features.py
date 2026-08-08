"""
==========================================================
Project : AI-Powered Real-Time Network Intrusion Detection
Module  : Feature Scaling
Author   : Anirudh Singh
==========================================================
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler

# ==========================================================
# PATHS
# ==========================================================

DATASET_DIR = Path("dataset/processed")

X_TRAIN_FILE = DATASET_DIR / "X_train.csv"
X_TEST_FILE = DATASET_DIR / "X_test.csv"

Y_TRAIN_FILE = DATASET_DIR / "y_train.csv"
Y_TEST_FILE = DATASET_DIR / "y_test.csv"

MODEL_DIR = Path("models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

SCALER_FILE = MODEL_DIR / "scaler.pkl"

REPORT_FILE = Path(
    "dataset/metadata/scaling_report.txt"
)

# ==========================================================
# LOAD DATA
# ==========================================================

def load_data():

    print("=" * 70)
    print("Loading Train/Test Dataset...")
    print("=" * 70)

    X_train = pd.read_csv(
        X_TRAIN_FILE
    )

    X_test = pd.read_csv(
        X_TEST_FILE
    )

    y_train = pd.read_csv(
        Y_TRAIN_FILE
    )

    y_test = pd.read_csv(
        Y_TEST_FILE
    )

    print(f"Train Shape : {X_train.shape}")
    print(f"Test Shape  : {X_test.shape}")

    return (

        X_train,

        X_test,

        y_train,

        y_test

    )

# ==========================================================
# FEATURE SCALING
# ==========================================================

def scale_features(

    X_train,

    X_test

):

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(
        X_train
    )

    X_test_scaled = scaler.transform(
        X_test
    )

    print("✔ Feature Scaling Completed")

    return (

        X_train_scaled,

        X_test_scaled,

        scaler

    )

# ==========================================================
# SAVE NUMPY FILES
# ==========================================================

def save_numpy(

    X_train,

    X_test,

    y_train,

    y_test

):

    np.save(

        DATASET_DIR /
        "X_train.npy",

        X_train

    )

    np.save(

        DATASET_DIR /
        "X_test.npy",

        X_test

    )

    np.save(

        DATASET_DIR /
        "y_train.npy",

        y_train.values.ravel()

    )

    np.save(

        DATASET_DIR /
        "y_test.npy",

        y_test.values.ravel()

    )

    print("✔ NumPy Files Saved")

    # ==========================================================
# SAVE SCALER
# ==========================================================

def save_scaler(scaler):

    joblib.dump(
        scaler,
        SCALER_FILE
    )

    print("✔ Scaler Saved")


# ==========================================================
# SAVE REPORT
# ==========================================================

def save_report(
    X_train,
    X_test
):

    with open(REPORT_FILE, "w") as file:

        file.write("=" * 70 + "\n")
        file.write("FEATURE SCALING REPORT\n")
        file.write("=" * 70 + "\n\n")

        file.write("Scaler : StandardScaler\n\n")

        file.write(f"Train Shape : {X_train.shape}\n")
        file.write(f"Test Shape  : {X_test.shape}\n\n")

        file.write(f"Train Samples : {len(X_train):,}\n")
        file.write(f"Test Samples  : {len(X_test):,}\n\n")

        file.write(f"Features : {X_train.shape[1]}\n")

    print("✔ Scaling Report Saved")


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 70)
    print("STARTING FEATURE SCALING")
    print("=" * 70)

    X_train, X_test, y_train, y_test = load_data()

    X_train_scaled, X_test_scaled, scaler = scale_features(
        X_train,
        X_test
    )

    save_numpy(
        X_train_scaled,
        X_test_scaled,
        y_train,
        y_test
    )

    save_scaler(scaler)

    save_report(
        X_train_scaled,
        X_test_scaled
    )

    print("\n" + "=" * 70)
    print("FEATURE SCALING COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print("\nGenerated Files")
    print("-" * 40)

    print("dataset/processed/X_train.npy")
    print("dataset/processed/X_test.npy")
    print("dataset/processed/y_train.npy")
    print("dataset/processed/y_test.npy")

    print(f"\nScaler : {SCALER_FILE}")
    print(f"Report : {REPORT_FILE}")


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    main()