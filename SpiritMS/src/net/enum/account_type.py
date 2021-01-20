from enum import Enum


class AccountType(Enum):
    Player = 0
    Tester = 1 << 5
    Intern = 1 << 3
    GameMaster = 1 << 4
    Admin = 1 << 4


def get_account_type_by_name(name):
    if name.lower() == "admin":
        return AccountType.Admin
    elif name.lower() == "player":
        return AccountType.Player
    elif name.lower() == "intern":
        return AccountType.Intern
    elif name.lower() == "tester":
        return AccountType.Tester

    return None
