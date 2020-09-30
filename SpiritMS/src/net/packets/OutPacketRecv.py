from numpy import byte, short

from src.net.debug import Debug
from src.net.packets.Packet import Packet
from PyByteBuffer import ByteBuffer

"""
OutHeaders, packets that are sent to Maple Client and decoded
@author Brandon
Created: 8/21/2020
"""

DEFAULT = 50


class OutPacketRecv(Packet):

    def __init__(self, opcode=None):
        super(Packet, self).__init__()
        self._buf_byte = ByteBuffer.allocate(DEFAULT)
        self._opcode = opcode

    def get_header(self):
        return self._opcode

    def encode_value(self, b):
        """
        :param b: byte, int, short, arrays
        :return:
        """
        self._buf_byte.put(b)

    def encode_string(self, s):
        if s is None:
            s = ""
        if len(s) > 32767:  # short max length
            Debug.error("Tried to encode a string that is too big")
            return
        self.encode_value(short(len(s)))  # encoding a short here
        self.o_encode_string(self, s=s, length=len(s))

    def o_encode_string(self, s, length):
        if s is None:
            s = ""
        if len(s) > 0:
            for c in s:
                self.encode_value(bytes(c))  # encoding a char, but actually writes as a byte
        i = len(s)
        while i < length:
            self.encode_value(bytes(0))
            i += 1
