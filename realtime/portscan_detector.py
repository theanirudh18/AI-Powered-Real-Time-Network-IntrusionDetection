"""
==========================================================
PortScan Detector
Detects rapid scans based on destination ports
==========================================================
"""


class PortScanDetector:

    def __init__(self, window=5, threshold=20):

        self.window = window
        self.threshold = threshold

        self.history = {}
        self.alerted = set()

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

            if src_ip in self.alerted:
                return None

            self.alerted.add(src_ip)

            return {
                "label": "PortScan",
                "confidence": 100.0,
                "source_ip": src_ip,
                "destination_ip": packet["dst_ip"],
                "protocol": packet["transport"],
                "ports_scanned": len(unique_ports)
            }

        return None