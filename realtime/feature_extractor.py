"""
==========================================================
Feature Extractor
Builds the feature vector for the trained model
==========================================================
"""

import json
from pathlib import Path

import numpy as np

from realtime.detector import Detector


class FeatureExtractor:

    def __init__(

        self,

        detector

    ):

        metadata = Path(

            "dataset/metadata/selected_features.json"

        )

        with open(

            metadata,

            "r"

        ) as file:

            data = json.load(file)

        self.feature_order = data["feature_order"]

        self.detector = detector

        print(
            f"Loaded {len(self.feature_order)} features."
        )

    # ======================================================
    # EXTRACT FEATURES
    # ======================================================

    def extract(

        self,

        flow

    ):

        feature_map = self.build_feature_map(

            flow

        )

        vector = []

        for feature in self.feature_order:

            vector.append(

                feature_map.get(

                    feature,

                    0.0

                )

            )

        return np.array(

            vector,

            dtype=np.float32

        )

    # ======================================================
    # PREDICT
    # ======================================================

    def predict(

        self,

        features,

        flow

    ):

        return self.detector.predict(

            features,

            flow

        )
            # ======================================================
    # BUILD FEATURE MAP
    # ======================================================
        # ======================================================
    # BUILD FEATURE MAP
    # ======================================================

    def build_feature_map(self, flow):

        return {

            # ==================================================
            # EXACT FEATURE ORDER (Training)
            # ==================================================

            "Destination Port": flow.destination_port,

            "Flow Duration": flow.duration,

            "Total Fwd Packets": flow.total_forward_packets,

            "Total Length of Fwd Packets": flow.total_forward_bytes,

            "Fwd Packet Length Max": flow.fwd_pkt_len_max,

            "Fwd Packet Length Min": flow.fwd_pkt_len_min,

            "Fwd Packet Length Mean": flow.fwd_pkt_len_mean,

            "Bwd Packet Length Max": flow.bwd_pkt_len_max,

            "Bwd Packet Length Min": flow.bwd_pkt_len_min,

            "Flow Bytes/s": flow.bytes_per_second,

            "Flow Packets/s": flow.packets_per_second,

            "Flow IAT Mean": flow.flow_iat_mean,

            "Flow IAT Std": flow.flow_iat_std,

            "Flow IAT Max": flow.flow_iat_max,

            "Flow IAT Min": flow.flow_iat_min,

            "Fwd IAT Mean": flow.fwd_iat_mean,

            "Fwd IAT Std": flow.fwd_iat_std,

            "Fwd IAT Min": flow.fwd_iat_min,

            "Bwd IAT Total": flow.bwd_iat_total,

            "Bwd IAT Mean": flow.bwd_iat_mean,

            "Bwd IAT Std": flow.bwd_iat_std,

            "Bwd IAT Max": flow.bwd_iat_max,

            "Bwd IAT Min": flow.bwd_iat_min,

            "Fwd PSH Flags": flow.fwd_psh_flags,

            "Fwd URG Flags": flow.fwd_urg_flags,

            "Fwd Header Length": flow.fwd_header_length,

            "Bwd Header Length": flow.bwd_header_length,

            "Bwd Packets/s": flow.bwd_packets_per_second,

            "Min Packet Length": flow.pkt_len_min,

            "Max Packet Length": flow.pkt_len_max,

            "Packet Length Mean": flow.pkt_len_mean,

            "Packet Length Variance": flow.pkt_len_variance,

            "FIN Flag Count": flow.fin_flag_count,

            "RST Flag Count": flow.rst_flag_count,

            "PSH Flag Count": flow.psh_flag_count,

            "ACK Flag Count": flow.ack_flag_count,

            "URG Flag Count": flow.urg_flag_count,

            "Down/Up Ratio": flow.down_up_ratio,

            "Init_Win_bytes_forward": flow.init_win_bytes_forward,

            "Init_Win_bytes_backward": flow.init_win_bytes_backward,

            "act_data_pkt_fwd": flow.act_data_pkt_fwd,

            "min_seg_size_forward": flow.min_seg_size_forward,

            "Active Mean": flow.active_mean,

            "Active Std": flow.active_std,

            "Active Max": flow.active_max,

            "Active Min": flow.active_min,

            "Idle Std": flow.idle_std

        }
        print("\n========== FEATURE MAP ==========")
        for k, v in feature_map.items():
           print(f"{k:35} : {v}")
        print("=================================\n")



    

        

        return feature_map