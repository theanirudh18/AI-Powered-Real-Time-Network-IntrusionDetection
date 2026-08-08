"""
==========================================================
Project : AI-Powered Real-Time Network Intrusion Detection
Module  : Model Training (V2)
==========================================================
"""

import sys
import json
from pathlib import Path

import numpy as np

from sklearn.utils.class_weight import compute_class_weight

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from training.model import build_model

from tensorflow.keras.callbacks import (
    EarlyStopping,
    ReduceLROnPlateau,
    ModelCheckpoint,
    CSVLogger
)

# ==========================================================
# PATHS
# ==========================================================

DATASET_DIR = Path("dataset/processed")

MODEL_DIR = Path("models/v2")
LOG_DIR = Path("logs/v2")

MODEL_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

MODEL_FILE = MODEL_DIR / "cnn_bilstm_attention_v2.keras"
HISTORY_FILE = MODEL_DIR / "history.json"

LOG_FILE = LOG_DIR / "training_log.csv"

X_TRAIN_FILE = DATASET_DIR / "X_train.npy"
X_TEST_FILE = DATASET_DIR / "X_test.npy"

Y_TRAIN_FILE = DATASET_DIR / "y_train.npy"
Y_TEST_FILE = DATASET_DIR / "y_test.npy"

# ==========================================================
# CONFIG
# ==========================================================

INPUT_SHAPE = (47, 1)

NUM_CLASSES = 15

BATCH_SIZE = 256

EPOCHS = 30

# ==========================================================
# LOAD DATASET
# ==========================================================

def load_dataset():

    print("=" * 70)
    print("Loading Dataset...")
    print("=" * 70)

    X_train = np.load(X_TRAIN_FILE)
    X_test = np.load(X_TEST_FILE)

    y_train = np.load(Y_TRAIN_FILE)
    y_test = np.load(Y_TEST_FILE)

    X_train = X_train.reshape(
        X_train.shape[0],
        X_train.shape[1],
        1
    )

    X_test = X_test.reshape(
        X_test.shape[0],
        X_test.shape[1],
        1
    )

    print("Train :", X_train.shape)
    print("Test  :", X_test.shape)

    return (
        X_train,
        X_test,
        y_train,
        y_test
    )

# ==========================================================
# CLASS WEIGHTS
# ==========================================================

def get_class_weights(y_train):

    classes = np.unique(y_train)

    weights = compute_class_weight(
        class_weight="balanced",
        classes=classes,
        y=y_train
    )

    class_weights = {
        int(c): float(w)
        for c, w in zip(classes, weights)
    }

    return class_weights

    # ==========================================================
# CALLBACKS
# ==========================================================

def get_callbacks():

    return [

        EarlyStopping(

            monitor="val_loss",

            patience=6,

            restore_best_weights=True,

            verbose=1

        ),

        ReduceLROnPlateau(

            monitor="val_loss",

            factor=0.2,

            patience=3,

            min_lr=1e-6,

            verbose=1

        ),

        ModelCheckpoint(

            filepath=MODEL_FILE,

            monitor="val_accuracy",

            save_best_only=True,

            save_weights_only=False,

            verbose=1

        ),

        CSVLogger(

            LOG_FILE,

            append=False

        )

    ]


# ==========================================================
# TRAIN
# ==========================================================

def train():

    X_train, X_test, y_train, y_test = load_dataset()

    class_weights = get_class_weights(
        y_train
    )

    model = build_model(

        input_shape=INPUT_SHAPE,

        num_classes=NUM_CLASSES

    )

    history = model.fit(

        X_train,

        y_train,

        validation_data=(

            X_test,

            y_test

        ),

        epochs=EPOCHS,

        batch_size=BATCH_SIZE,

        class_weight=class_weights,

        callbacks=get_callbacks(),

        shuffle=True,

        verbose=1

    )

    return (

        model,

        history

    )
    # ==========================================================
# SAVE HISTORY
# ==========================================================

def save_history(history):

    history_dict = {}

    for key, value in history.history.items():

        history_dict[key] = [

            float(v)

            for v in value

        ]

    with open(

        HISTORY_FILE,

        "w"

    ) as file:

        json.dump(

            history_dict,

            file,

            indent=4

        )

    print("✔ History Saved")


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 70)
    print("CNN + BiLSTM + BAHDANAU ATTENTION TRAINING (V2)")
    print("=" * 70)

    model, history = train()

    save_history(history)

    print("\n" + "=" * 70)
    print("TRAINING COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print("\nGenerated Files")
    print("-" * 40)

    print(MODEL_FILE)
    print(HISTORY_FILE)
    print(LOG_FILE)


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    main()