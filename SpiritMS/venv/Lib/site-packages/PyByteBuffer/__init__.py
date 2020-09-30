"""
    PyByteBuffer - A bytes manipulation library inspired by Java ByteBuffer

    Copyright (C) 2019  Giovanni Rocca (iGio90)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import binascii

from PyByteBuffer import utils


class ByteBuffer(object):
    """
    Object class wrapping a byte array and allowing manipulation
    """
    def __init__(self):
        self.buffer = None
        """ the data buffer """
        self.position = 0
        """ current position """
        self.remaining = 0
        """ remaining bytes """

    @staticmethod
    def allocate(n):
        """
        return a `ByteBuffer` object wrapping an empty buffer of size `n`
        """
        d = bytearray([00] * n)
        b = ByteBuffer()
        b.__init(d)
        return b

    @staticmethod
    def from_hex(hex_str):
        """
        return a `ByteBuffer` object wrapping a buffer decoded from `hex_str`
        """
        b = ByteBuffer()
        b.__init(binascii.unhexlify(hex_str))
        return b

    @staticmethod
    def wrap(data):
        """
        return a `ByteBuffer` object wrapping `data`
        """
        b = ByteBuffer()
        b.__init(data)
        return b

    def __init(self, data):
        """
        Initialize this buffer with `data`
        """
        if type(data) is not bytearray:
            data = bytearray(data)

        self.buffer = data
        self.position = 0
        self.remaining = len(data)

    def _check_buffer(self, space):
        """
        check whether this buffer has enough `space` left for r/w op
        """
        return not self.remaining < space

    def _read(self, length=1):
        """
        for internal usage, read `length` byte from `buffer` and update position
        """
        assert self._check_buffer(length), 'Buffer has not enough bytes to read'
        r = self.buffer[self.position:self.position + length]
        self._update_offsets(length)
        return r

    def _update_offsets(self, value):
        """
        update `position` and `remaining` with the given `value`
        """
        self.position += value
        self.remaining -= value

    def array(self, length=0):
        """
        return a `bytearray` object of the required `length` and increment `position`
        """
        if length != 0 and length > self.remaining:
            length = self.remaining
        if length == 0:
            length = self.remaining
        r = self.buffer[self.position:self.position + length]
        self._update_offsets(len(r))
        return r

    def get(self, length=1, endianness='big'):
        """
        return the `int` representation of bytes starting at `position` for the given `length` and `endianness`.
        increment `position` after read.
        default `length` is 1 and big `endianness`
        """
        return int.from_bytes(self._read(length=length), byteorder=endianness)

    def put(self, value, size=0, endianness='big'):
        """
        write `value` in the buffer and increment `position`
        the data to write could be a string, an int, an array, a bytes/bytearray object, a list etc.
        optionally, you can specify an `endianness` if b is of type int.
        """
        t = type(value)
        if t == str:
            b = value.encode('utf8')
        elif t == int:
            if size == 0:
                size = utils.int_size(value)
            b = int.to_bytes(value, size, byteorder=endianness)
        elif t == list:
            b = bytes(value)
        elif t == bytes or t == bytearray:
            b = t
        else:
            raise Exception('Attempting to write unknown object into Buffer')
        l = len(b)
        assert self._check_buffer(l), 'Buffer has not enough space left'
        for i in range(l):
            self.buffer[self.position + i:self.position + i + 1] = b[i:i + 1]
        self._update_offsets(l)

    def rewind(self):
        """
        set `position` to 0
        """
        self.position = 0
        self.remaining = len(self.buffer)

    def slice(self):
        """
        slice `buffer` at current position.

        note:
            original `buffer` remain untouched.
            `position` is not incremented.
        """
        b = ByteBuffer()
        b.__init(self.buffer[self.position:])
        return b

    def split(self):
        """
        split this `buffer` at current position.
        returning a `Buffer` object starting from current position until `buffer` length.
        original `Buffer` is cutted at current position
        """
        b = self.slice()
        self.strip()
        return b

    def strip(self):
        """
        strip `Buffer` at current position.
        this remove all the bytes from current position until `buffer` length and set the new length to current position
        """
        self.buffer = self.buffer[:self.position]
        self.remaining = 0


__all__ = [
    "__title__", "__summary__", "__uri__", "__version__", "__author__",
    "__email__", "__license__", "__copyright__", "ByteBuffer",
]

__title__ = "PyByteBuffer"
__summary__ = "A bytes manipulation library inspired by Java ByteBuffer"
__uri__ = "https://github.com/iGio90/PyByteBuffer"

__version__ = "1.0.4"

__author__ = "iGio90"
__email__ = "giovanni.rocca.90@gmail.com"

__license__ = "GPL 3.0"
__copyright__ = "Copyright 2019 {0}".format(__author__)
