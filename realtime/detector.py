"""
==========================================================
Real-Time Detector
Loads Model + Scaler + Label Encoder
==========================================================
"""

import joblib
import numpy as np

from tensorflow.keras.models import load_model

import config

from realtime.websocket import add_detection

from training.layers.attention import BahdanauAttention
from training.focal_loss import SparseCategoricalFocalLoss

class Detector:

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

        print()

        print("======================================")

        print(" Real-Time Detector Loaded ")

        print("======================================")

        print()

    # ======================================================
    # PREPROCESS
    # ======================================================

    def preprocess(

        self,

        features

    ):

        features = np.asarray(

            features,

            dtype=np.float32

        ).reshape(

            1,

            -1

        )

        features = self.scaler.transform(

            features

        )

        features = features.reshape(

            1,

            features.shape[1],

            1

        )

        return features

    # ======================================================
    # PREDICT
    # ======================================================

    def predict(

        self,

        features,

        flow

    ):

        print("\n============= FEATURE VECTOR =============")

        for i, (name, value) in enumerate(zip(config.FEATURES, features)):
          print(f"{i:02d}. {name:30} = {value}")

        print("==========================================")   

        X = self.preprocess(

            features

        )

        probabilities = self.model.predict(

            X,

            verbose=0

        )
        print("\n========== CLASS PROBABILITIES ==========")

        for i, p in enumerate(probabilities[0]):
          label = self.encoder.inverse_transform([i])[0]
          print(f"{label:25} : {float(p):.6f}")

        print("=========================================\n")

        prediction_id = int(

            np.argmax(

                probabilities

            )

        )

        confidence = float(

            np.max(

                probabilities

            )

        )

        label = self.encoder.inverse_transform(

            [

                prediction_id

            ]

        )[0]
        print("\n=========== FLOW DEBUG ===========")
        print(f"Src IP        : {flow.src_ip}")
        print(f"Dst IP        : {flow.dst_ip}")
        print(f"Src Port      : {flow.src_port}")
        print(f"Dst Port      : {flow.dst_port}")
        print(f"Protocol      : {flow.transport}")
        print(f"Total Packets : {flow.total_packets}")
        print(f"Duration      : {flow.duration}")
        print("==================================")
        result = {

            "label": label,

            "confidence": round(

                confidence * 100,

                2

            ),

            "prediction_id": prediction_id,

            "probabilities": probabilities[0].tolist(),

            "source_ip": flow.src_ip,

            "destination_ip": flow.dst_ip,

            "source_port": flow.src_port,

            "destination_port": flow.dst_port,

            "protocol": flow.transport,

            "duration": round(

                flow.duration,

                6

            )

        }

        # ============================================
        # LIVE OUTPUT
        # ============================================

        print()

        print("=" * 60)

        print("REAL-TIME DETECTION")

        print("=" * 60)

        print(f"Source IP        : {result['source_ip']}")

        print(f"Destination IP   : {result['destination_ip']}")

        print(f"Protocol         : {result['protocol']}")

        print(f"Prediction       : {result['label']}")

        print(f"Confidence       : {result['confidence']}%")

        print("=" * 60)

        print()

        add_detection(result)

        return result

# ==========================================================
# TEST
# ==========================================================

def main():

    detector = Detector()

    dummy = np.zeros(

        47,

        dtype=np.float32

    )

    class DummyFlow:

        src_ip = "192.168.1.100"

        dst_ip = "192.168.1.200"

        src_port = 45000

        dst_port = 80

        transport = "TCP"

        duration = 0.25

    result = detector.predict(

        dummy,

        DummyFlow()

    )

    print(result)


if __name__ == "__main__":

    main()