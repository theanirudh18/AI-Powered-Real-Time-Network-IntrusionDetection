"""
==========================================================
Flow Object
Stores packets belonging to a single network flow
==========================================================
"""

import statistics


class Flow:

    def __init__(

        self,

        first_packet

    ):

        self.src_ip = first_packet["src_ip"]

        self.dst_ip = first_packet["dst_ip"]

        self.src_port = first_packet["src_port"]

        self.dst_port = first_packet["dst_port"]

        self.protocol = first_packet["protocol"]

        self.transport = first_packet["transport"]

        self.start_time = first_packet["timestamp"]

        self.last_time = first_packet["timestamp"]

        self.forward_packets = []

        self.backward_packets = []
        self.active_periods = []
        self.idle_periods = []
        self.last_packet_time = self.start_time

        self.add_packet(

            first_packet

        )

    # ======================================================
    # ADD PACKET
    # ======================================================
    

    def add_packet(

        self,

        packet

    ):

        self.last_time = packet["timestamp"]
        gap = packet["timestamp"] - self.last_packet_time

        if gap > 1.0:
         self.idle_periods.append(gap)
        else:
         self.active_periods.append(gap)

         self.last_packet_time = packet["timestamp"]

        if (

            packet["src_ip"] == self.src_ip

            and

            packet["src_port"] == self.src_port

        ):

            self.forward_packets.append(

                packet

            )

        else:

            self.backward_packets.append(

                packet

            )

    # ======================================================
    # ALL PACKETS
    # ======================================================

    @property

    def packets(

        self

    ):

        return (

            self.forward_packets +

            self.backward_packets

        )
            # ======================================================
    # FLOW DURATION
    # ======================================================

    @property
    def duration(self):

        return max(

            self.last_time - self.start_time,

            0.0

        )

    # ======================================================
    # PACKET COUNTS
    # ======================================================

    @property
    def total_forward_packets(self):

        return len(

            self.forward_packets

        )

    @property
    def total_backward_packets(self):

        return len(

            self.backward_packets

        )

    @property
    def total_packets(self):

        return (

            self.total_forward_packets +

            self.total_backward_packets

        )

    # ======================================================
    # BYTE COUNTS
    # ======================================================

    @property
    def total_forward_bytes(self):

        return sum(

            packet["length"]

            for packet in self.forward_packets

        )

    @property
    def total_backward_bytes(self):

        return sum(

            packet["length"]

            for packet in self.backward_packets

        )

    @property
    def total_bytes(self):

        return (

            self.total_forward_bytes +

            self.total_backward_bytes

        )

    # ======================================================
    # PACKET LENGTHS
    # ======================================================

    def forward_lengths(self):

        return [

            packet["length"]

            for packet in self.forward_packets

        ]

    def backward_lengths(self):

        return [

            packet["length"]

            for packet in self.backward_packets

        ]

    def all_lengths(self):

        return [

            packet["length"]

            for packet in self.packets

        ]
            # ======================================================
    # LENGTH STATISTICS
    # ======================================================

    @staticmethod
    def _safe_max(values):

        return max(values) if values else 0

    @staticmethod
    def _safe_min(values):

        return min(values) if values else 0

    @staticmethod
    def _safe_mean(values):

        return statistics.mean(values) if values else 0

    @staticmethod
    def _safe_std(values):

        return statistics.stdev(values) if len(values) > 1 else 0

    @staticmethod
    def _safe_var(values):

        return statistics.variance(values) if len(values) > 1 else 0

    # ======================================================
    # FORWARD PACKET LENGTH STATS
    # ======================================================

    @property
    def fwd_pkt_len_max(self):

        return self._safe_max(self.forward_lengths())

    @property
    def fwd_pkt_len_min(self):

        return self._safe_min(self.forward_lengths())

    @property
    def fwd_pkt_len_mean(self):

        return self._safe_mean(self.forward_lengths())

    @property
    def fwd_pkt_len_std(self):

        return self._safe_std(self.forward_lengths())

    # ======================================================
    # BACKWARD PACKET LENGTH STATS
    # ======================================================

    @property
    def bwd_pkt_len_max(self):

        return self._safe_max(self.backward_lengths())

    @property
    def bwd_pkt_len_min(self):

        return self._safe_min(self.backward_lengths())

    @property
    def bwd_pkt_len_mean(self):

        return self._safe_mean(self.backward_lengths())

    @property
    def bwd_pkt_len_std(self):

        return self._safe_std(self.backward_lengths())

    # ======================================================
    # OVERALL PACKET LENGTH STATS
    # ======================================================

    @property
    def pkt_len_max(self):

        return self._safe_max(self.all_lengths())

    @property
    def pkt_len_min(self):

        return self._safe_min(self.all_lengths())

    @property
    def pkt_len_mean(self):

        return self._safe_mean(self.all_lengths())

    @property
    def pkt_len_std(self):

        return self._safe_std(self.all_lengths())

    @property
    def pkt_len_variance(self):

        return self._safe_var(self.all_lengths())
            # ======================================================
    # INTER ARRIVAL TIMES (IAT)
    # ======================================================

    @staticmethod
    def _iat(times):

     if len(times) < 2:
        return []

     times = sorted(times)

     return [

        times[i] - times[i - 1]

        for i in range(1, len(times))

     ]

    # ======================================================
    # TIMESTAMP LISTS
    # ======================================================

    def forward_times(self):

        return [

            packet["timestamp"]

            for packet in self.forward_packets

        ]

    def backward_times(self):

        return [

            packet["timestamp"]

            for packet in self.backward_packets

        ]

    def all_times(self):

      return sorted(

        packet["timestamp"]

        for packet in self.packets

      ) 

    # ======================================================
    # FLOW IAT
    # ======================================================

    @property
    def flow_iat(self):

        return self._iat(

            self.all_times()

        )

    @property
    def flow_iat_mean(self):

        return self._safe_mean(

            self.flow_iat

        )

    @property
    def flow_iat_std(self):

        return self._safe_std(

            self.flow_iat

        )

    @property
    def flow_iat_max(self):

        return self._safe_max(

            self.flow_iat

        )

    @property
    def flow_iat_min(self):

        return self._safe_min(

            self.flow_iat

        )

    # ======================================================
    # FORWARD IAT
    # ======================================================

    @property
    def fwd_iat(self):

        return self._iat(

            self.forward_times()

        )

    @property
    def fwd_iat_mean(self):

        return self._safe_mean(

            self.fwd_iat

        )

    @property
    def fwd_iat_std(self):

        return self._safe_std(

            self.fwd_iat

        )

    @property
    def fwd_iat_max(self):

        return self._safe_max(

            self.fwd_iat

        )

    @property
    def fwd_iat_min(self):

        return self._safe_min(

            self.fwd_iat

        )

    # ======================================================
    # BACKWARD IAT
    # ======================================================

    @property
    def bwd_iat(self):

        return self._iat(

            self.backward_times()

        )

    @property
    def bwd_iat_mean(self):

        return self._safe_mean(

            self.bwd_iat

        )

    @property
    def bwd_iat_std(self):

        return self._safe_std(

            self.bwd_iat

        )

    @property
    def bwd_iat_max(self):

        return self._safe_max(

            self.bwd_iat

        )

    @property
    def bwd_iat_min(self):

        return self._safe_min(

            self.bwd_iat

        )
            # ======================================================
    # TCP FLAG COUNTS
    # ======================================================

    def _flag_count(self, mask):

        count = 0

        for packet in self.packets:

            if packet["flags"] & mask:

                count += 1

        return count

    @property
    def fin_flag_count(self):

        return self._flag_count(0x01)

    @property
    def syn_flag_count(self):

        return self._flag_count(0x02)

    @property
    def rst_flag_count(self):

        return self._flag_count(0x04)

    @property
    def psh_flag_count(self):

        return self._flag_count(0x08)

    @property
    def ack_flag_count(self):

        return self._flag_count(0x10)

    @property
    def urg_flag_count(self):

        return self._flag_count(0x20)

    # ======================================================
    # FLOW RATES
    # ======================================================

    @property
    def packets_per_second(self):

        if self.duration <= 0:

            return 0

        return self.total_packets / self.duration

    @property
    def bytes_per_second(self):

        if self.duration <= 0:

            return 0

        return self.total_bytes / self.duration

    # ======================================================
    # ACTIVE / IDLE TIMES
    # ======================================================

    @property
    def active_times(self):

       return self.active_periods if self.active_periods else [0]


    @property
    def idle_times(self):

      return self.idle_periods if self.idle_periods else [0]

    @property
    def active_mean(self):

        return self._safe_mean(self.active_times)

    @property
    def active_std(self):

        return self._safe_std(self.active_times)

    @property
    def active_max(self):

        return self._safe_max(self.active_times)

    @property
    def active_min(self):

        return self._safe_min(self.active_times)

    @property
    def idle_mean(self):

        return self._safe_mean(self.idle_times)

    @property
    def idle_std(self):

        return self._safe_std(self.idle_times)

    @property
    def idle_max(self):

        return self._safe_max(self.idle_times)

    @property
    def idle_min(self):

        return self._safe_min(self.idle_times)
            # ======================================================
    # DESTINATION PORT
    # ======================================================

    @property
    def destination_port(self):

        return self.dst_port

    # ======================================================
    # BACKWARD IAT TOTAL
    # ======================================================

    @property
    def bwd_iat_total(self):

        return sum(self.bwd_iat)

    # ======================================================
    # FORWARD PSH FLAGS
    # ======================================================

    @property
    def fwd_psh_flags(self):

        count = 0

        for packet in self.forward_packets:

            if packet["flags"] & 0x08:

                count += 1

        return count

    # ======================================================
    # FORWARD URG FLAGS
    # ======================================================

    @property
    def fwd_urg_flags(self):

        count = 0

        for packet in self.forward_packets:

            if packet["flags"] & 0x20:

                count += 1

        return count

    # ======================================================
    # HEADER LENGTHS
    # ======================================================

    @property
    def fwd_header_length(self):

        return sum(

            packet["ip_header_length"] +

            packet["tcp_header_length"]

            for packet in self.forward_packets

        )

    @property
    def bwd_header_length(self):

        return sum(

            packet["ip_header_length"] +

            packet["tcp_header_length"]

            for packet in self.backward_packets

        )

    # ======================================================
    # BACKWARD PACKETS / SECOND
    # ======================================================

    @property
    def bwd_packets_per_second(self):

        if self.duration <= 0:

            return 0

        return self.total_backward_packets / self.duration

    # ======================================================
    # DOWN / UP RATIO
    # ======================================================

    @property
    def down_up_ratio(self):

        if self.total_forward_packets == 0:

            return 0

        return (

            self.total_backward_packets /

            self.total_forward_packets

        )

    # ======================================================
    # INITIAL WINDOW SIZE
    # ======================================================

    @property
    def init_win_bytes_forward(self):

        if not self.forward_packets:

            return 0

        return self.forward_packets[0]["window_size"]

    @property
    def init_win_bytes_backward(self):

        if not self.backward_packets:

            return 0

        return self.backward_packets[0]["window_size"]

    # ======================================================
    # ACTIVE DATA PACKETS
    # ======================================================

    @property
    def act_data_pkt_fwd(self):

        count = 0

        for packet in self.forward_packets:

            if packet["payload_length"] > 0:

                count += 1

        return count

    # ======================================================
    # MIN SEGMENT SIZE
    # ======================================================

    @property
    def min_seg_size_forward(self):

        if not self.forward_packets:

            return 0

        return min(

            packet["tcp_header_length"]

            for packet in self.forward_packets

        )