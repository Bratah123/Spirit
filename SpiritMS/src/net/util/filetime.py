from enum import Enum
from typing import Tuple


class FileTimeType(Enum):
    MAX_TIME = 35120710, -1157267456
    ZERO_TIME = 21968699, -35635200
    FT_UT_OFFSET = 116444592000000000
    QUEST_TIME = 27111903
    PLAIN_ZERO = 0


class FileTime:
    def __init__(self, time: FileTimeType, is_converted_for_client: bool = True):
        self.high_date_time = 0
        self.low_date_time = 0
        self.time = time.value

        if isinstance(self.time, Tuple):
            self.low_date_time = self.time[0]
            self.high_date_time = self.time[1]
        else:
            self.low_date_time = int(self.time)
            self.high_date_time = int(self.time >> 32)

        self.is_converted_for_client = is_converted_for_client

    def to_long(self):
        return self.low_date_time & 0xFFFFFFFF | (self.high_date_time << 32)

    def encode(self, out_packet):
        if not self.is_converted_for_client:
            out_packet.encode_long(self.to_long() * 10000 + 116444736000000000)  # Out of index issues most likely
        else:
            out_packet.encode_int(int(self.high_date_time))
            out_packet.encode_int(int(self.low_date_time))
