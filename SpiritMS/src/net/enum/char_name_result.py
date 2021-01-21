from enum import Enum


class CharNameResult(Enum):
    Available = 0
    Unavailable_InUse = 1
    Unavailable_Invalid = 2
    Unavailable_CashItem = 3