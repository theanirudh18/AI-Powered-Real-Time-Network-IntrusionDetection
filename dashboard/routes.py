"""
==========================================================
Dashboard Routes
==========================================================
"""

from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    send_from_directory
)

import config
from flask import jsonify

from realtime.websocket import get_results, get_stats, get_attack_history

from dashboard.services import PredictionService


dashboard = Blueprint(

    "dashboard",

    __name__

)


service = PredictionService()


# ==========================================================
# HOME
# ==========================================================

@dashboard.route("/")

def home():

    return render_template(

        "index.html"

    )


# ==========================================================
# ABOUT
# ==========================================================

@dashboard.route("/about")

def about():

    return render_template(

        "about.html"

    )


# ==========================================================
# REALTIME
# ==========================================================

@dashboard.route("/realtime")

def realtime():

    return render_template(

        "realtime.html"

    )


# ==========================================================
# UPLOAD
# ==========================================================

@dashboard.route(
    "/upload",
    methods=["POST"]
)
def upload():

    if "file" not in request.files:

        flash("Please upload a CSV file.")

        return redirect(
            url_for("dashboard.home")
        )

    try:

        result = service.predict(
            request.files["file"]
        )

        summary = result["summary"]

    except Exception as e:

        raise
        # Later we'll change this back to:
        # flash(str(e))
        # return redirect(url_for("dashboard.home"))

    return render_template(

        "result.html",

        filename=result["filename"],

        prediction_file=result["prediction_file"],

        total_flows=summary["total_flows"],

        benign=summary["benign"],

        attacks=summary["attacks"],

        attack_types=summary["attack_types"],

        confidence=summary["average_confidence"]

    )

# ==========================================================
# DOWNLOAD
# ==========================================================

@dashboard.route(

    "/download/<filename>"

)

def download(filename):

    return send_from_directory(

        config.RESULT_DIR,

        filename,

        as_attachment=True

    )
    # ==========================================================
# LIVE DETECTIONS
# ==========================================================

@dashboard.route("/live-packets")
def live_packets():

    return jsonify(

        get_results()

    )


# ==========================================================
# LIVE STATS (PERMANENT, NEVER RESETS)
# ==========================================================

@dashboard.route("/live-stats")
def live_stats():

    return jsonify(

        get_stats()

    )


# ==========================================================
# ATTACK HISTORY (PERSISTS, NEVER CLEARED BY NORMAL TRAFFIC)
# ==========================================================

@dashboard.route("/attack-history")
def attack_history():

    return jsonify(

        get_attack_history()

    )


# ==========================================================
# HEALTH CHECK
# ==========================================================

@dashboard.route("/health")
def health():

    return jsonify(

        {

            "status": "running",

            "service": "AI Real-Time IDS"

        }

    )