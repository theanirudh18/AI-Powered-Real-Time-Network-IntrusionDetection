"""
==========================================================
PortScan Detector
Detects rapid scans based on destination ports
==========================================================
"""


class PortScanDetector:

    def __init__(self, window=5, threshold=20, cooldown=15):

        self.window = window
        self.threshold = threshold
        self.cooldown = cooldown  # seconds before the same IP can alert again

        self.history = {}
        self.last_alert_time = {}

    def process_packet(self, packet):

        src_ip = packet["src_ip"]
        now = packet["timestamp"]

        if src_ip not in self.history:
            self.history[src_ip] = []

        self.history[src_ip].append(
            (now, packet["dst_port"])
        )

        # Remove old entries
        self.history[src_ip] = [
            x
            for x in self.history[src_ip]
            if now - x[0] <= self.window
        ]

        unique_ports = {
            port
            for _, port in self.history[src_ip]
        }

        if len(unique_ports) >= self.threshold:

            last_alert = self.last_alert_time.get(src_ip)

            if last_alert is not None and (now - last_alert) < self.cooldown:
                return None

            self.last_alert_time[src_ip] = now

            return {
                "label": "PortScan",
                "confidence": 100.0,
                "source_ip": src_ip,
                "destination_ip": packet["dst_ip"],
                "protocol": packet["transport"],
                "ports_scanned": len(unique_ports),
                "timestamp": now
            }

        return None
