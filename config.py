"""
==========================================================
AI Powered Real-Time Network Intrusion Detection System
Configuration File
==========================================================
"""

from pathlib import Path

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

# ==========================================================
# DIRECTORIES
# ==========================================================

MODEL_DIR = BASE_DIR / "models"

UPLOAD_DIR = BASE_DIR / "uploads"

RESULT_DIR = BASE_DIR / "results"

TEMPLATE_DIR = BASE_DIR / "templates"

STATIC_DIR = BASE_DIR / "static"

# ==========================================================
# MODEL FILES
# ==========================================================

MODEL_PATH = MODEL_DIR / "cnn_bilstm_attention.keras"

SCALER_PATH = MODEL_DIR / "scaler.pkl"

LABEL_ENCODER_PATH = MODEL_DIR / "label_encoder.pkl"

# ==========================================================
# FLASK
# ==========================================================

SECRET_KEY = "AI_REALTIME_IDS_SECRET"

HOST = "127.0.0.1"

PORT = 8000

DEBUG = True

# ==========================================================
# PREDICTION
# ==========================================================

CONFIDENCE_DECIMALS = 2

PREDICTION_FILE = "predictions.csv"

# ==========================================================
# MODEL INPUT FEATURES
# ==========================================================

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

# ==========================================================
# CREATE DIRECTORIES
# ==========================================================

UPLOAD_DIR.mkdir(exist_ok=True)

RESULT_DIR.mkdir(exist_ok=True)