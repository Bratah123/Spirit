"""
Represents a packet to be sent over a TCP socket for Maplestory.
Applies extra functionality because it is a Maplestory Packet

Ported over from SwordieMS to Python SpiritMS src
@author Brandon
Created 8/21/2020
"""
import copy

from numpy.core import byte

from src.net.util import Util


class Packet:

    def __init__(self, data):
        self._data = byte(data.length)
        self._data = [copy.deepcopy(x) for x in data[0:len(data)]]

    def get_length(self):
        if self._data is not None:
            return len(self._data)
        return 0

    def get_header(self):
        if self.get_length() < 2:
            return 0xFFFF
        return self._data[0] + (self._data[1] << 8)

    # TODO: Decorators

    def set_data(self, new_data):
        self._data = new_data

    def get_data(self):
        return self._data

    def to_string(self):
        if self._data is None:
            return ""
        return f"[PACKET] {Util.readable_byte_arr(self._data)}"

    def clone(self):
        new_packet = Packet(self._data)
        return new_packet

    def release(self):
        pass
