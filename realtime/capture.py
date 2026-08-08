"""
==========================================================
Packet Capture Engine
==========================================================
"""

from queue import Queue
from threading import Thread

from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP


class PacketCapture:

    def __init__(self, flow_manager):

        self.queue = Queue()
        self.flow_manager = flow_manager
        self.running = False

    # ======================================================
    # START CAPTURE
    # ======================================================

    def start(self, interface=None):

        self.running = True

        worker = Thread(
            target=self.process_packets,
            daemon=True
        )

        worker.start()

        sniff(
            iface=interface,
            prn=self.capture_packet,
            store=False
        )

    # ======================================================
    # STOP
    # ======================================================

    def stop(self):

        self.running = False

    # ======================================================
    # CALLBACK
    # ======================================================

    def capture_packet(self, packet):

     if IP not in packet:
        return

     ip = packet[IP]

     if TCP in packet:
        tcp = packet[TCP]
        print(f"TCP {ip.src}:{tcp.sport} -> {ip.dst}:{tcp.dport}")

     elif UDP in packet:
        udp = packet[UDP]
        print(f"UDP {ip.src}:{udp.sport} -> {ip.dst}:{udp.dport}")

     self.queue.put(packet)

    # ======================================================
    # PROCESS QUEUE
    # ======================================================

    def process_packets(self):

        while self.running:

            packet = self.queue.get()

            try:

                packet_info = self.extract_packet(packet)

                if packet_info:

                    self.flow_manager.process_packet(
                        packet_info
                    )

            except Exception as e:

                print("[Capture Error]", e)

    # ======================================================
    # EXTRACT PACKET
    # ======================================================

    def extract_packet(self, packet):

        ip = packet[IP]

        packet_info = {

            "timestamp": float(packet.time),

            "src_ip": ip.src,

            "dst_ip": ip.dst,

            "protocol": ip.proto,

            "length": len(packet),

            "ttl": ip.ttl,

            "src_port": 0,

            "dst_port": 0,

            "flags": 0,

            "transport": "OTHER",

            "ip_header_length": (
                ip.ihl * 4
                if hasattr(ip, "ihl") and ip.ihl
                else 20
            ),

            "tcp_header_length": 0,

            "window_size": 0,

            "payload_length": 0

        }

        if TCP in packet:

            tcp = packet[TCP]

            packet_info["transport"] = "TCP"

            packet_info["src_port"] = tcp.sport

            packet_info["dst_port"] = tcp.dport

            packet_info["flags"] = int(tcp.flags)

            packet_info["window_size"] = int(tcp.window)

            packet_info["tcp_header_length"] = tcp.dataofs * 4

            packet_info["payload_length"] = len(bytes(tcp.payload))

        elif UDP in packet:

            udp = packet[UDP]

            packet_info["transport"] = "UDP"

            packet_info["src_port"] = udp.sport

            packet_info["dst_port"] = udp.dport

            packet_info["payload_length"] = len(bytes(udp.payload))

        return packet_info

    # ======================================================
    # STATS
    # ======================================================

    def stats(self):

        return {

            "queue_size": self.queue.qsize(),

            "active_flows": len(self.flow_manager.flows),

            "running": self.running

        }


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("capture.py loaded successfully")