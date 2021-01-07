from enum import Enum

"""
    Credits: Rooba, for packet handling in python
"""


class DebugType(Enum):
    _byte = 0x1
    _short = 0x2
    _int = 0x4
    _long = 0x8
    _string = 0x10
