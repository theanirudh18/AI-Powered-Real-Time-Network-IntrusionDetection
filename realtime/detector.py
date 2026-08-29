"""
==========================================================
Real-Time Detector
Loads Model + Scaler + Label Encoder
==========================================================
"""

import joblib
import numpy as np
import time

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

        # Locate the attention layer instance once, so we can read its
        # weights after every prediction without searching layers each time.
        self.attention_layer = None

        for layer in self.model.layers:

            if isinstance(layer, BahdanauAttention):

                self.attention_layer = layer

                break

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

        # NOTE: model(X, training=False) is used instead of model.predict(X)
        # because .predict() runs inside a compiled tf.function graph, where
        # the attention layer's self.last_attention_weights would only ever
        # capture a symbolic placeholder rather than real values. A direct
        # eager call re-runs the layer's Python code every time, so we get
        # the actual numbers back.
        probabilities = self.model(

            X,

            training=False

        ).numpy()

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

        # ============================================
        # ATTENTION EXPLAINABILITY
        # ============================================

        top_features = []

        if self.attention_layer is not None and \
           getattr(self.attention_layer, "last_attention_weights", None) is not None:

            weights = self.attention_layer.last_attention_weights.numpy()

            weights = weights.reshape(-1)  # (47,)

            ranked = sorted(
                zip(config.FEATURES, weights),
                key=lambda pair: pair[1],
                reverse=True
            )[:5]

            top_features = [
                {"feature": name, "weight": round(float(w) * 100, 2)}
                for name, w in ranked
            ]

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

            ),

            "timestamp": time.time(),

            "top_features": top_features

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

        if top_features:
            print("Top Features     :", ", ".join(
                f"{f['feature']} ({f['weight']}%)" for f in top_features[:3]
            ))

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