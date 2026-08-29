"""
==========================================================
Live Detection Buffer
==========================================================
"""

from collections import deque

from realtime.alerts import send_email_alert

CONFIDENCE_THRESHOLD = 70.0  # below this, a non-BENIGN label is treated as "uncertain"

LIVE_RESULTS = deque(maxlen=100)

ATTACK_HISTORY = deque(maxlen=200)

TOTAL_STATS = {
    "total": 0,
    "benign": 0,
    "attacks": 0,
    "uncertain": 0
}

def add_detection(result):

    LIVE_RESULTS.appendleft(result)

    TOTAL_STATS["total"] += 1

    label = result.get("label")
    confidence = float(result.get("confidence", 0))

    if label == "BENIGN":
        TOTAL_STATS["benign"] += 1

    elif confidence < CONFIDENCE_THRESHOLD:
        TOTAL_STATS["uncertain"] += 1

    else:
        TOTAL_STATS["attacks"] += 1
        ATTACK_HISTORY.appendleft(result)
        send_email_alert(result)

def get_results():

    return list(LIVE_RESULTS)

def get_stats():

    return dict(TOTAL_STATS)

def get_attack_history():

    return list(ATTACK_HISTORY)