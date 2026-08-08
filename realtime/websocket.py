"""
==========================================================
Live Detection Buffer
==========================================================
"""

from collections import deque

LIVE_RESULTS = deque(maxlen=100)

def add_detection(result):

    LIVE_RESULTS.appendleft(result)

def get_results():

    return list(LIVE_RESULTS)