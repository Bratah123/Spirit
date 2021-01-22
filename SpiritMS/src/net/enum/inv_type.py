from enum import Enum


class InvType(Enum):
    EQUIPPED = -1
    EQUIP = 1
    CONSUME = 2
    ETC = 4
    INSTALL = 3
    CASH = 5


def get_inv_type_by_name(name):
    inv_types = {
        'equipped': InvType.EQUIPPED,
        'equip': InvType.EQUIP,
        'eqp': InvType.EQUIP,
        'consume': InvType.CONSUME,
        'use': InvType.CONSUME,
        'etc': InvType.ETC,
        'install': InvType.INSTALL,
        'setup': InvType.INSTALL,
        'cash': InvType.CASH
    }

    return inv_types.get(name.lower())
