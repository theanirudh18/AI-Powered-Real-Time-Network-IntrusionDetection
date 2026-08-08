"""
==========================================================
AI-Powered Real-Time Network Intrusion Detection
Main Flask Application
==========================================================
"""

import threading

from flask import Flask

from dashboard.routes import dashboard

from realtime.detector import Detector
from realtime.feature_extractor import FeatureExtractor
from realtime.flow_manager import FlowManager
from realtime.capture import PacketCapture

# ==========================================================
# CREATE FLASK APP
# ==========================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = "ai-realtime-ids"

# ==========================================================
# INITIALIZE AI PIPELINE
# ==========================================================

print()

print("=" * 60)
print(" Initializing AI IDS...")
print("=" * 60)

detector = Detector()

extractor = FeatureExtractor(
    detector
)

flow_manager = FlowManager(
    extractor
)

capture = PacketCapture(
    flow_manager
)

print("✔ AI Pipeline Ready")

print("=" * 60)
print()

# ==========================================================
# START REAL-TIME PACKET CAPTURE
# ==========================================================

def start_capture():

    print()

    print("=" * 60)
    print(" Starting Packet Capture...")
    print("=" * 60)

    try:

        capture.start()

    except KeyboardInterrupt:

        print()

        print("Packet Capture Stopped")

    except Exception as error:

        print()

        print("Capture Error :")

        print(error)


capture_thread = threading.Thread(

    target=start_capture,

    daemon=True

)

capture_thread.start()

print("✔ Packet Capture Thread Started")

print()
# ==========================================================
# REGISTER BLUEPRINTS
# ==========================================================


app.register_blueprint(

    dashboard

)
print("✔ Dashboard Routes Registered")

# ==========================================================
# ERROR HANDLERS
# ==========================================================

@app.errorhandler(404)
def page_not_found(error):

    return "404 - Page Not Found", 404


@app.errorhandler(500)
def internal_server_error(error):

    return "500 - Internal Server Error", 500


# ==========================================================
# LIVE HEALTH CHECK
# ==========================================================

@app.route("/health")
def health():

    return {

        "status": "running",

        "model": "loaded",

        "capture": "active"

    }
    # ==========================================================
# RUN FLASK SERVER
# ==========================================================

if __name__ == "__main__":

    print()

    print("=" * 60)
    print(" AI Real-Time IDS Dashboard")
    print("=" * 60)

    print("Running at : http://127.0.0.1:8000")

    print("=" * 60)

    app.run(

        host="0.0.0.0",

        port=8000,

        debug=True,

        use_reloader=False

    )