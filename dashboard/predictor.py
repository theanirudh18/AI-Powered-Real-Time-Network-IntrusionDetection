"""
==========================================================
Prediction Engine
==========================================================
"""

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import joblib
import numpy as np
import pandas as pd

from tensorflow.keras.models import load_model

import config

from training.layers.attention import BahdanauAttention
from training.focal_loss import SparseCategoricalFocalLoss


class Predictor:

    def __init__(self):

        self.model = load_model(
            config.MODEL_PATH,
            custom_objects={
                "BahdanauAttention": BahdanauAttention,
                "SparseCategoricalFocalLoss": SparseCategoricalFocalLoss
            },
            compile=False
        )

        self.scaler = joblib.load(
            config.SCALER_PATH
        )

        self.encoder = joblib.load(
            config.LABEL_ENCODER_PATH
        )

        self.features = [f.strip() for f in config.FEATURES]

        print("✅ Model Loaded Successfully")

    # ==========================================================
    # LOAD CSV
    # ==========================================================

    def load_csv(self, csv_file):

        df = pd.read_csv(csv_file)

        # Remove leading/trailing spaces from column names
        df.columns = df.columns.str.strip()

        return df

    # ==========================================================
    # VALIDATE FEATURES
    # ==========================================================

    def validate(self, df):

        missing = [
            feature
            for feature in self.features
            if feature not in df.columns
        ]

        if missing:

            raise ValueError(
                "Missing Columns:\n" +
                "\n".join(missing)
            )

        return True

    # ==========================================================
    # PREPROCESS
    # ==========================================================

    def preprocess(self, df):

        X = df[self.features].copy()

        X.replace(
            [np.inf, -np.inf],
            np.nan,
            inplace=True
        )

        X.fillna(
            0,
            inplace=True
        )

        X = self.scaler.transform(X)

        X = X.reshape(
            X.shape[0],
            X.shape[1],
            1
        )

        return X

    # ==========================================================
    # PREDICT
    # ==========================================================

    def predict(self, csv_file, output_folder):

        # ---------------------------
        # Load CSV
        # ---------------------------

        df = self.load_csv(csv_file)

        # ---------------------------
        # Validate
        # ---------------------------

        self.validate(df)

        # ---------------------------
        # Preprocess
        # ---------------------------

        X = self.preprocess(df)

        # ---------------------------
        # Prediction
        # ---------------------------

        probabilities = self.model.predict(
            X,
            verbose=0
        )

        prediction_ids = np.argmax(
            probabilities,
            axis=1
        )

        confidence = np.max(
            probabilities,
            axis=1
        )

        predictions = self.encoder.inverse_transform(
            prediction_ids
        )

        # ---------------------------
        # Result DataFrame
        # ---------------------------

        result_df = df.copy()

        result_df["Prediction"] = predictions

        result_df["Confidence"] = np.round(
            confidence * 100,
            config.CONFIDENCE_DECIMALS
        )

        # ---------------------------
        # Statistics
        # ---------------------------

        total_flows = len(result_df)

        benign = int(
            (result_df["Prediction"] == "BENIGN").sum()
        )

        attacks = total_flows - benign

        attack_types = (
            result_df["Prediction"]
            .value_counts()
            .to_dict()
        )

        average_confidence = round(
            float(result_df["Confidence"].mean()),
            config.CONFIDENCE_DECIMALS
        )

        # ---------------------------
        # Save Results
        # ---------------------------

        output_folder = Path(output_folder)

        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = (
            output_folder /
            config.PREDICTION_FILE
        )

        result_df.to_csv(
            output_file,
            index=False
        )

        # ---------------------------
        # Summary
        # ---------------------------

        summary = {

            "total_flows": total_flows,
            "benign": benign,
            "attacks": attacks,
            "attack_types": attack_types,
            "average_confidence": average_confidence

        }

        return summary, str(output_file)


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    predictor = Predictor()

    print("\n======================================")
    print(" Predictor Ready ")
    print("======================================\n")