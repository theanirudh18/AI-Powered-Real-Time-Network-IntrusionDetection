"""
==========================================================
Project : AI-Powered Real-Time Network Intrusion Detection
Module  : CNN + BiLSTM + Bahdanau Attention (V2)
==========================================================
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

from tensorflow.keras.layers import (

    Input,

    Conv1D,

    BatchNormalization,

    Activation,

    Add,

    MaxPooling1D,

    SpatialDropout1D,

    Bidirectional,

    LSTM,

    LayerNormalization,

    Dense,

    Dropout

)

try:

    from training.layers.attention import BahdanauAttention
    from training.focal_loss import SparseCategoricalFocalLoss

except ModuleNotFoundError:

    from training.layers.attention import BahdanauAttention
    from training.focal_loss import SparseCategoricalFocalLoss


# ==========================================================
# BUILD MODEL
# ==========================================================

def build_model(

    input_shape=(47, 1),

    num_classes=15

):

    inputs = Input(

        shape=input_shape,

        name="Input"

    )

    # ======================================================
    # RESIDUAL CNN BLOCK
    # ======================================================

    shortcut = Conv1D(

        filters=64,

        kernel_size=1,

        padding="same"

    )(inputs)

    x = Conv1D(

        filters=64,

        kernel_size=3,

        padding="same"

    )(inputs)

    x = BatchNormalization()(x)

    x = Activation("relu")(x)

    x = Conv1D(

        filters=64,

        kernel_size=3,

        padding="same"

    )(x)

    x = BatchNormalization()(x)

    x = Add()([

        x,

        shortcut

    ])

    x = Activation("relu")(x)

    x = MaxPooling1D(

        pool_size=2

    )(x)

    x = SpatialDropout1D(

        rate=0.20

    )(x)
        # ======================================================
    # BiLSTM BLOCK
    # ======================================================

    x = Bidirectional(

        LSTM(

            units=128,

            return_sequences=True,

            dropout=0.30,

            recurrent_dropout=0.20

        ),

        name="BiLSTM"

    )(x)

    x = LayerNormalization(

        name="LayerNorm"

    )(x)

    # ======================================================
    # BAHDANAU ATTENTION
    # ======================================================

    x = BahdanauAttention(

        units=128,

        name="BahdanauAttention"

    )(x)

    # ======================================================
    # CLASSIFIER
    # ======================================================

    x = Dense(

        128,

        activation="relu",

        name="Dense_1"

    )(x)

    x = Dropout(

        0.40,

        name="Dropout_1"

    )(x)

    x = Dense(

        64,

        activation="relu",

        name="Dense_2"

    )(x)

    x = Dropout(

        0.20,

        name="Dropout_2"

    )(x)

    outputs = Dense(

        num_classes,

        activation="softmax",

        name="Output"

    )(x)

    model = Model(

        inputs=inputs,

        outputs=outputs,

        name="CNN_BiLSTM_Bahdanau_V2"

    )
        # ======================================================
    # COMPILE MODEL
    # ======================================================

    model.compile(

        optimizer=Adam(
            learning_rate=0.001
        ),

        loss=SparseCategoricalFocalLoss(
            gamma=2.0,
            alpha=0.25
        ),

        metrics=[
            "accuracy"
        ]

    )

    return model


# ==========================================================
# MODEL SUMMARY
# ==========================================================

if __name__ == "__main__":

    model = build_model()

    model.summary()