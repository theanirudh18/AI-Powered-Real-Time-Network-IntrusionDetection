"""
==========================================================
Project : AI-Powered Real-Time Network Intrusion Detection
Module  : Model Evaluation
==========================================================
"""

from pathlib import Path
import json
import time
import joblib
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

from tensorflow.keras.models import load_model

import sys

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from training.layers.attention import BahdanauAttention
except ModuleNotFoundError:
    import sys
    from pathlib import Path

    ROOT = Path(__file__).resolve().parent.parent

    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

    from training.layers.attention import BahdanauAttention
# ==========================================================
# PATHS
# ==========================================================

DATASET_DIR = Path("dataset/processed")

MODEL_DIR = Path("models")

REPORT_DIR = Path("reports/v2")

GRAPH_DIR = Path("graphs/v2")

REPORT_DIR.mkdir(parents=True, exist_ok=True)

GRAPH_DIR.mkdir(parents=True, exist_ok=True)

MODEL_FILE = MODEL_DIR / "cnn_bilstm_attention.keras"

HISTORY_FILE = MODEL_DIR / "history.json"

LABEL_ENCODER = MODEL_DIR / "label_encoder.pkl"

X_TEST = DATASET_DIR / "X_test.npy"
Y_TEST = DATASET_DIR / "y_test.npy"

# ==========================================================
# LOAD
# ==========================================================

def load_data():

    X = np.load(X_TEST)
    y = np.load(Y_TEST)

    X = X.reshape(
        X.shape[0],
        X.shape[1],
        1
    )

    try:
        encoder = joblib.load(MODEL_DIR / "label_encoder.pkl")
    except:
        encoder = joblib.load(Path("models/label_encoder.pkl"))

    from training.focal_loss import SparseCategoricalFocalLoss

    model = load_model(
        MODEL_FILE,
        custom_objects={
            "BahdanauAttention": BahdanauAttention,
            "SparseCategoricalFocalLoss": SparseCategoricalFocalLoss
        },
        compile=False
    )

    return X, y, encoder, model
# ==========================================================
# PREDICTION
# ==========================================================

def predict(model, X):

    start = time.perf_counter()

    probabilities = model.predict(
        X,
        verbose=0
    )

    end = time.perf_counter()

    prediction = np.argmax(
        probabilities,
        axis=1
    )

    inference = (end - start) / len(X)

    return prediction, probabilities, inference


# ==========================================================
# METRICS
# ==========================================================

def calculate_metrics(y_true, y_pred):

    metrics = {

        "accuracy": accuracy_score(
            y_true,
            y_pred
        ),

        "precision_macro": precision_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0
        ),

        "recall_macro": recall_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0
        ),

        "f1_macro": f1_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0
        ),

        "precision_weighted": precision_score(
            y_true,
            y_pred,
            average="weighted",
            zero_division=0
        ),

        "recall_weighted": recall_score(
            y_true,
            y_pred,
            average="weighted",
            zero_division=0
        ),

        "f1_weighted": f1_score(
            y_true,
            y_pred,
            average="weighted",
            zero_division=0
        )

    }

    return metrics

    # ==========================================================
# SAVE METRICS
# ==========================================================

def save_metrics(metrics, inference):

    metrics["inference_time_per_sample_sec"] = inference

    model_size = MODEL_FILE.stat().st_size / (1024 * 1024)
    metrics["model_size_mb"] = round(model_size, 2)

    with open(REPORT_DIR / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)

    print("✔ Metrics Saved")


# ==========================================================
# CLASSIFICATION REPORT
# ==========================================================

def save_classification_report(
    y_true,
    y_pred,
    encoder
):

    report = classification_report(
        y_true,
        y_pred,
        target_names=encoder.classes_,
        digits=4,
        zero_division=0
    )

    with open(
        REPORT_DIR / "classification_report.txt",
        "w"
    ) as f:

        f.write(report)

    print("✔ Classification Report Saved")


# ==========================================================
# CONFUSION MATRIX
# ==========================================================

def save_confusion_matrix(
    y_true,
    y_pred,
    encoder
):

    cm = confusion_matrix(
        y_true,
        y_pred
    )

    np.savetxt(
        REPORT_DIR / "confusion_matrix.csv",
        cm,
        fmt="%d",
        delimiter=","
    )

    plt.figure(figsize=(12,10))

    plt.imshow(
        cm,
        interpolation="nearest"
    )

    plt.colorbar()

    plt.xticks(
        np.arange(len(encoder.classes_)),
        encoder.classes_,
        rotation=90,
        fontsize=8
    )

    plt.yticks(
        np.arange(len(encoder.classes_)),
        encoder.classes_,
        fontsize=8
    )

    plt.xlabel("Predicted")

    plt.ylabel("Actual")

    plt.title("Confusion Matrix")

    plt.tight_layout()

    plt.savefig(
        GRAPH_DIR / "confusion_matrix.png",
        dpi=300
    )

    plt.close()

    print("✔ Confusion Matrix Saved")


# ==========================================================
# TRAINING GRAPHS
# ==========================================================

def save_training_graphs():

    history_file = HISTORY_FILE

    if not history_file.exists():
        return

    with open(history_file) as f:
        history = json.load(f)

    # Accuracy

    plt.figure(figsize=(8,5))

    plt.plot(history["accuracy"])

    plt.plot(history["val_accuracy"])

    plt.legend([
        "Train",
        "Validation"
    ])

    plt.xlabel("Epoch")

    plt.ylabel("Accuracy")

    plt.title("Training Accuracy")

    plt.tight_layout()

    plt.savefig(
        GRAPH_DIR / "training_accuracy.png",
        dpi=300
    )

    plt.close()

    # Loss

    plt.figure(figsize=(8,5))

    plt.plot(history["loss"])

    plt.plot(history["val_loss"])

    plt.legend([
        "Train",
        "Validation"
    ])

    plt.xlabel("Epoch")

    plt.ylabel("Loss")

    plt.title("Training Loss")

    plt.tight_layout()

    plt.savefig(
        GRAPH_DIR / "training_loss.png",
        dpi=300
    )

    plt.close()

    print("✔ Training Graphs Saved")


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 70)
    print("MODEL EVALUATION")
    print("=" * 70)

    X, y, encoder, model = load_data()

    y_pred, probabilities, inference = predict(
        model,
        X
    )

    metrics = calculate_metrics(
        y,
        y_pred
    )

    save_metrics(
        metrics,
        inference
    )

    save_classification_report(
        y,
        y_pred,
        encoder
    )

    save_confusion_matrix(
        y,
        y_pred,
        encoder
    )

    save_training_graphs()

    print("\n" + "=" * 70)
    print("EVALUATION COMPLETED")
    print("=" * 70)

    print(f"\nAccuracy : {metrics['accuracy']:.4f}")
    print(f"Macro F1 : {metrics['f1_macro']:.4f}")
    print(f"Weighted F1 : {metrics['f1_weighted']:.4f}")


# ==========================================================
# ENTRY
# ==========================================================

if __name__ == "__main__":
    main()