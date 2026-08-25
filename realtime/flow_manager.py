"""
==========================================================
Flow Manager
Maintains Active Network Flows
==========================================================
"""

import time
from realtime.portscan_detector import PortScanDetector

from realtime.flow import Flow
from realtime.websocket import add_detection


class FlowManager:

    def __init__(self, extractor):

        self.flows = {}

        self.timeout = 3

        self.extractor = extractor
        self.portscan_detector = PortScanDetector()

    # ======================================================
    # FLOW KEY
    # ======================================================

    def get_flow_key(self, packet):

        end1 = (packet["src_ip"], packet["src_port"])
        end2 = (packet["dst_ip"], packet["dst_port"])

        if end1 <= end2:
          return (end1, end2, packet["protocol"])
        else:
          return (end2, end1, packet["protocol"])

    # ======================================================
    # PROCESS PACKET
    # ======================================================
    def process_packet(self, packet):

      result = self.portscan_detector.process_packet(packet)

      if result:

        print()

        print("=" * 60)
        print("PORTSCAN DETECTED")
        print("=" * 60)
        print(f"Source IP        : {result['source_ip']}")
        print(f"Destination IP   : {result['destination_ip']}")
        print(f"Protocol         : {result['protocol']}")
        print(f"Ports Scanned    : {result['ports_scanned']}")
        print("=" * 60)
        print()

        add_detection({

            "label": "PortScan",

            "confidence": 100.0,

            "source_ip": result["source_ip"],

            "destination_ip": result["destination_ip"],

            "source_port": "-",

            "destination_port": "-",

            "protocol": result["protocol"],

            "duration": 0,

            "ports_scanned": result["ports_scanned"],

            "timestamp": result.get("timestamp", time.time())

        })


      flow_key = self.get_flow_key(packet)

      if flow_key not in self.flows:

        self.flows[flow_key] = Flow(packet)

      else:

        self.flows[flow_key].add_packet(packet)

      self.cleanup()
    

    # ======================================================
    # CLEANUP EXPIRED FLOWS
    # ======================================================

    def cleanup(self):

        current_time = time.time()

        expired = []

        for flow_key, flow in self.flows.items():

            idle_time = current_time - flow.last_time

            if idle_time >= self.timeout:

                expired.append(flow_key)

        for flow_key in expired:

            flow = self.flows[flow_key]

            try:

                features = self.extractor.extract(flow)

                if features is not None:

                    self.extractor.predict(

                        features,

                        flow

                    )

            except Exception as e:

                print("[Flow Error]", e)

            del self.flows[flow_key]

    # ======================================================
    # FORCE FLUSH
    # ======================================================

    def flush(self):

        keys = list(self.flows.keys())

        for key in keys:

            flow = self.flows[key]

            try:

                features = self.extractor.extract(flow)

                if features is not None:

                    self.extractor.predict(

                        features,

                        flow

                    )

            except Exception as e:

                print("[Flush Error]", e)

            del self.flows[key]

    # ======================================================
    # FLOW STATISTICS
    # ======================================================

    def stats(self):

        total_packets = 0

        tcp_flows = 0

        udp_flows = 0

        other_flows = 0

        for flow in self.flows.values():

            total_packets += flow.total_packets

            if flow.protocol == 6:

                tcp_flows += 1

            elif flow.protocol == 17:

                udp_flows += 1

            else:

                other_flows += 1

        return {

            "active_flows": len(self.flows),

            "total_packets": total_packets,

            "tcp_flows": tcp_flows,

            "udp_flows": udp_flows,

            "other_flows": other_flows

        }

    # ======================================================
    # GET FLOW
    # ======================================================

    def get_flow(self, flow_key):

        return self.flows.get(flow_key)

    # ======================================================
    # REMOVE FLOW
    # ======================================================

    def remove_flow(self, flow_key):

        if flow_key in self.flows:

            del self.flows[flow_key]

    # ======================================================
    # CLEAR
    # ======================================================

    def clear(self):

        self.flows.clear()


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("FlowManager loaded successfully.")
