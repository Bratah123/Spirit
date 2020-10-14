"""
Represents a packet to be sent over a TCP socket for Maplestory.
Applies extra functionality because it is a Maplestory Packet

Ported over from SwordieMS to Python SpiritMS src
@author Brandon
Created 8/21/2020
"""
from src.net.packets.byte_buffer.ByteBuffer import ByteBuffer
from src.net.util import Util
from src.net.packets.OutPackets import OutPacket


class Packet(ByteBuffer):
    """
        Packet class used to send/receive from client
        Parameters
        data: bytes
            The initial data to load into the packet
        opcode: InPackets/OutPackets values
    """

    def __init__(self, data=None, opcode=None, raw=False):

        self._data = None
        if data is None:
            data = b''

        super().__init__(data)
        if not data:
            self.opcode = opcode
            # check if a number is provided rather than an ENUM from In/Out Packets
            if isinstance(self.opcode, int):
                # we encode in the init so we don't have to encode in the handler part
                self.encode_short(self.opcode)
            else:
                self.encode_short(self.opcode.value)
            return
        if raw:
            return

        self.opcode = OutPacket(self.decode_short())

    @property
    def name(self):
        if isinstance(self.opcode, int):
            return self.opcode
        return self.opcode.name

    def to_array(self):
        return self.getvalue()

    def __len__(self):
        return len(self.getvalue())

    def get_length(self):
        if self._data is not None:
            return len(self._data)
        return 0

    def get_header(self):
        if self.get_length() < 2:
            return 0xFFFF
        return self._data[0] + (self._data[1] << 8)

    def to_string(self):
        return Util.to_string(self.getvalue())

    def clone(self):
        new_packet = Packet(self.data)
        return new_packet
