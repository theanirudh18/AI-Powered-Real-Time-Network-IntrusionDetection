"""
==========================================================
Project : AI-Powered Real-Time Network Intrusion Detection
Module  : Train Test Split
Author  : Anirudh Singh
==========================================================
"""

from pathlib import Path
import pandas as pd

from sklearn.model_selection import train_test_split

# ==========================================================
# PATHS
# ==========================================================

INPUT_FILE = Path("dataset/processed/encoded_dataset.csv")

OUTPUT_DIR = Path("dataset/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_FILE = Path("dataset/metadata/split_report.txt")

# ==========================================================
# CONFIG
# ==========================================================

TEST_SIZE = 0.20
RANDOM_STATE = 42

# ==========================================================
# LOAD DATASET
# ==========================================================

def load_dataset():

    print("=" * 70)
    print("Loading Encoded Dataset...")
    print("=" * 70)

    df = pd.read_csv(
        INPUT_FILE,
        low_memory=False
    )

    print(f"Dataset Shape : {df.shape}")

    return df

# ==========================================================
# TRAIN TEST SPLIT
# ==========================================================

def split_dataset(df):

    X = df.drop(
        columns=["Label"]
    )

    y = df["Label"]

    X_train, X_test, y_train, y_test = train_test_split(

        X,

        y,

        test_size=TEST_SIZE,

        random_state=RANDOM_STATE,

        stratify=y,

        shuffle=True

    )

    print("\nTrain/Test Split Completed")

    print(f"Train Samples : {len(X_train):,}")
    print(f"Test Samples  : {len(X_test):,}")

    return (
        X_train,
        X_test,
        y_train,
        y_test
    )

# ==========================================================
# SAVE CSV FILES
# ==========================================================

def save_csv_files(
    X_train,
    X_test,
    y_train,
    y_test
):

    X_train.to_csv(
        OUTPUT_DIR / "X_train.csv",
        index=False
    )

    X_test.to_csv(
        OUTPUT_DIR / "X_test.csv",
        index=False
    )

    y_train.to_frame().to_csv(
        OUTPUT_DIR / "y_train.csv",
        index=False
    )

    y_test.to_frame().to_csv(
        OUTPUT_DIR / "y_test.csv",
        index=False
    )

    print("✔ Train/Test CSV Files Saved")

    # ==========================================================
# SAVE REPORT
# ==========================================================

def save_report(
    X_train,
    X_test,
    y_train,
    y_test
):

    train_dist = (
        y_train.value_counts()
        .sort_index()
    )

    test_dist = (
        y_test.value_counts()
        .sort_index()
    )

    with open(REPORT_FILE, "w") as file:

        file.write("=" * 70 + "\n")
        file.write("TRAIN TEST SPLIT REPORT\n")
        file.write("=" * 70 + "\n\n")

        file.write(f"Train Samples : {len(X_train):,}\n")
        file.write(f"Test Samples  : {len(X_test):,}\n\n")

        file.write(f"Features : {X_train.shape[1]}\n")
        file.write(f"Classes  : {len(train_dist)}\n\n")

        file.write("=" * 50 + "\n")
        file.write("TRAIN CLASS DISTRIBUTION\n")
        file.write("=" * 50 + "\n")

        for label, count in train_dist.items():
            file.write(f"{label:>2} : {count:,}\n")

        file.write("\n")

        file.write("=" * 50 + "\n")
        file.write("TEST CLASS DISTRIBUTION\n")
        file.write("=" * 50 + "\n")

        for label, count in test_dist.items():
            file.write(f"{label:>2} : {count:,}\n")

    print("✔ Split Report Saved")


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 70)
    print("STARTING TRAIN TEST SPLIT")
    print("=" * 70)

    df = load_dataset()

    X_train, X_test, y_train, y_test = split_dataset(df)

    save_csv_files(
        X_train,
        X_test,
        y_train,
        y_test
    )

    save_report(
        X_train,
        X_test,
        y_train,
        y_test
    )

    print("\n" + "=" * 70)
    print("TRAIN TEST SPLIT COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print("\nGenerated Files")
    print("-" * 40)

    print("dataset/processed/X_train.csv")
    print("dataset/processed/X_test.csv")
    print("dataset/processed/y_train.csv")
    print("dataset/processed/y_test.csv")

    print(f"\nReport : {REPORT_FILE}")


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    main()