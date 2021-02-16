from enum import Enum
from io import BytesIO
from struct import unpack, pack
from typing import List

from src.net.util.filetime import FileTime
from src.net.util.position import Position


class ByteBuffer(BytesIO):
    """
        Base class for packet's write and read operations
    """

    def __init__(self, initial_bytes):
        super().__init__(initial_bytes)
        self._string_len = 0

    def encode(self, _bytes):
        self.write(_bytes)
        return self

    def encode_byte(self, value):
        if isinstance(value, Enum):
            value = value.value
        if value > 128:
            self.encode_unsigned_byte(value)
            return self
        self.write(pack('b', value))
        return self

    def encode_unsigned_byte(self, value):
        if isinstance(value, Enum):
            value = value.value
        self.write(pack('B', value))

    def encode_short(self, value):
        self.write(pack('H', value))
        return self

    def encode_unsigned_int(self, value):
        self.write(pack('I', value))
        return self

    def encode_int(self, value):
        self.write(pack('i', value))
        return self

    def encode_long(self, value):
        self.write(pack('Q', value))
        return self

    def encode_buffer(self, buffer):
        self.write(buffer)
        return self

    def skip(self, count):
        self.write(bytes(count))
        return self

    def encode_string(self, string):
        self.write(pack('H', len(string)))

        for ch in string:
            self.write(ch.encode())

        return self

    def encode_fixed_string(self, string, length):
        if string is None:
            string = ""

        string_length = len(string)

        if string_length > 0:
            for c in string:
                self.write(c.encode())

        for i in range(string_length, length):
            self.encode_byte(0)

        return self

    def encode_hex_string(self, string):
        string = string.strip(' -')
        self.write(bytes.fromhex(string))
        return self

    def encode_ft(self, filetime: FileTime):
        if filetime is None:
            self.encode_long(0)
        else:
            filetime.encode(self)

    def encode_position(self, position: Position):
        if position is not None:
            self.encode_short(position.x)
            self.encode_short(position.y)
        else:
            self.encode_short(0)
            self.encode_short(0)

    def encode_arr(self, aob: List):
        for b in aob:
            self.encode_byte(b)
        return self

    def decode_byte(self):
        return self.read(1)[0]

    def decode_bool(self):
        return bool(self.decode_byte())

    def decode_short(self):
        return unpack('H', self.read(2))[0]

    def decode_int(self):
        return unpack('I', self.read(4))[0]

    def decode_long(self):
        return unpack('Q', self.read(8))[0]

    def decode_buffer(self, size):
        return self.read(size)

    def decode_string(self) -> str:
        length = self.decode_short()
        string = ""

        for _ in range(length):
            string += self.read(1).decode()

        return string
