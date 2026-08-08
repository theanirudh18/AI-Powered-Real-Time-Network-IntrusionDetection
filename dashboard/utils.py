"""
==========================================================
Dashboard Utility Functions
==========================================================
"""

from pathlib import Path
import numpy as np
import pandas as pd


FEATURES = [

    "Destination Port",
    "Flow Duration",
    "Total Fwd Packets",
    "Total Length of Fwd Packets",
    "Fwd Packet Length Max",
    "Fwd Packet Length Min",
    "Fwd Packet Length Mean",
    "Bwd Packet Length Max",
    "Bwd Packet Length Min",
    "Flow Bytes/s",
    "Flow Packets/s",
    "Flow IAT Mean",
    "Flow IAT Std",
    "Flow IAT Max",
    "Flow IAT Min",
    "Fwd IAT Mean",
    "Fwd IAT Std",
    "Fwd IAT Min",
    "Bwd IAT Total",
    "Bwd IAT Mean",
    "Bwd IAT Std",
    "Bwd IAT Max",
    "Bwd IAT Min",
    "Fwd PSH Flags",
    "Fwd URG Flags",
    "Fwd Header Length",
    "Bwd Header Length",
    "Bwd Packets/s",
    "Min Packet Length",
    "Max Packet Length",
    "Packet Length Mean",
    "Packet Length Variance",
    "FIN Flag Count",
    "RST Flag Count",
    "PSH Flag Count",
    "ACK Flag Count",
    "URG Flag Count",
    "Down/Up Ratio",
    "Init_Win_bytes_forward",
    "Init_Win_bytes_backward",
    "act_data_pkt_fwd",
    "min_seg_size_forward",
    "Active Mean",
    "Active Std",
    "Active Max",
    "Active Min",
    "Idle Std"

]


def verify_features(df):

    missing = [

        feature

        for feature in FEATURES

        if feature not in df.columns

    ]

    return missing


def clean_dataframe(df):

    df = df.copy()

    df = df[FEATURES]

    df.replace(

        [np.inf, -np.inf],

        np.nan,

        inplace=True

    )

    df.fillna(

        0,

        inplace=True

    )

    return df


def save_predictions(df, output_file):

    output_file = Path(output_file)

    output_file.parent.mkdir(

        parents=True,

        exist_ok=True

    )

    df.to_csv(

        output_file,

        index=False

    )

    return str(output_file)


def generate_summary(df):

    total_flows = len(df)

    benign = int(

        (df["Prediction"] == "BENIGN").sum()

    )

    attacks = total_flows - benign

    attack_types = (

        df["Prediction"]

        .value_counts()

        .to_dict()

    )

    average_confidence = round(

        float(

            df["Confidence"].mean()

        ),

        2

    )

    return {

        "total_flows": total_flows,

        "benign": benign,

        "attacks": attacks,

        "attack_types": attack_types,

        "average_confidence": average_confidence

    }


if __name__ == "__main__":

    print("Dashboard Utils Loaded Successfully")