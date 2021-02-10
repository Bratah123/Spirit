"""
Credits to Sjonnie
"""
from src.net.packets.byte_buffer.packet import Packet


class ExtendSP:
    def __init__(
            self,
            extend_sp_id=0,
            sub_jobs=0,
    ):
        self._extend_sp_id = extend_sp_id
        self._sp_set = []
        i = 1
        while i <= sub_jobs:
            self._sp_set.append(SPSet(job_level=i))
            i += 1

    @property
    def sp_set(self):
        return self._sp_set

    @property
    def extend_sp_id(self):
        return self._extend_sp_id

    def get_sp_set_size(self):
        return len(self.sp_set)

    def encode(self, out_packet: Packet):
        out_packet.encode_byte(self.get_sp_set_size())
        for sps in self.sp_set:
            out_packet.encode_byte(sps.job_level)
            out_packet.encode_int(sps.sp)


class SPSet:
    def __init__(
            self,
            sp_set_id=0,
            job_level=0,
            sp=0,
    ):
        self._sp_set_id = sp_set_id
        self._job_level = job_level
        self._sp = sp

    @property
    def job_level(self):
        return self._job_level

    @property
    def sp(self):
        return self._sp
