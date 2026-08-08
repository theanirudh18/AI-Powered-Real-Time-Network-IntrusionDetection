"""
==========================================================
Project : AI-Powered Real-Time Network Intrusion Detection
Module  : Label Encoding
Author  : Anirudh Singh

Description:
    Encodes attack labels using LabelEncoder.

Outputs:
    - encoded_dataset.csv
    - label_encoder.pkl
    - label_mapping.json
    - label_encoding_report.txt
==========================================================
"""

from pathlib import Path
import json
import joblib
import pandas as pd

from sklearn.preprocessing import LabelEncoder

# ==========================================================
# PATHS
# ==========================================================

INPUT_FILE = Path("dataset/interim/selected_dataset.csv")

OUTPUT_FILE = Path("dataset/processed/encoded_dataset.csv")

MODEL_DIR = Path("models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

METADATA_DIR = Path("dataset/metadata")
METADATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

ENCODER_FILE = MODEL_DIR / "label_encoder.pkl"

MAPPING_FILE = METADATA_DIR / "label_mapping.json"

REPORT_FILE = METADATA_DIR / "label_encoding_report.txt"

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

    print(f"Dataset Shape : {df.shape}")

    return df


# ==========================================================
# LABEL ENCODING
# ==========================================================

def encode_labels(df):

    encoder = LabelEncoder()

    df["Label"] = encoder.fit_transform(
        df["Label"]
    )

    print(
        f"Total Classes : {len(encoder.classes_)}"
    )

    return df, encoder


# ==========================================================
# SAVE LABEL ENCODER
# ==========================================================

def save_encoder(encoder):

    joblib.dump(
        encoder,
        ENCODER_FILE
    )

    print("✔ Label Encoder Saved")


# ==========================================================
# SAVE LABEL MAPPING
# ==========================================================

def save_mapping(encoder):

    mapping = {}

    for index, label in enumerate(
        encoder.classes_
    ):

        mapping[int(index)] = label

    with open(
        MAPPING_FILE,
        "w"
    ) as file:

        json.dump(
            mapping,
            file,
            indent=4
        )

    print("✔ Label Mapping Saved")
    # ==========================================================
# SAVE ENCODED DATASET
# ==========================================================

def save_dataset(df):

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("✔ Encoded Dataset Saved")


# ==========================================================
# SAVE REPORT
# ==========================================================

def save_report(df, encoder):

    with open(REPORT_FILE, "w") as file:

        file.write("=" * 70 + "\n")
        file.write("LABEL ENCODING REPORT\n")
        file.write("=" * 70 + "\n\n")

        file.write(f"Rows : {df.shape[0]:,}\n")
        file.write(f"Columns : {df.shape[1]}\n\n")

        file.write(f"Total Classes : {len(encoder.classes_)}\n\n")

        file.write("Class Mapping\n")
        file.write("-" * 50 + "\n")

        for index, label in enumerate(encoder.classes_):
            file.write(f"{index:>2}  -->  {label}\n")

    print("✔ Label Encoding Report Saved")


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 70)
    print("STARTING LABEL ENCODING")
    print("=" * 70)

    df = load_dataset()

    df, encoder = encode_labels(df)

    save_dataset(df)

    save_encoder(encoder)

    save_mapping(encoder)

    save_report(df, encoder)

    print("\n" + "=" * 70)
    print("LABEL ENCODING COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print(f"\nEncoded Dataset : {OUTPUT_FILE}")
    print(f"Label Encoder   : {ENCODER_FILE}")
    print(f"Label Mapping   : {MAPPING_FILE}")
    print(f"Report          : {REPORT_FILE}")


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    main()