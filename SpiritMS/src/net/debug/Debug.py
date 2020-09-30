from src.net.server import ServerConstants


def logs(string):
    if ServerConstants.DEBUG_MODE:
        print(f"[DEBUG] {string}")


def error(string):
    if ServerConstants.DEBUG_MODE:
        print(f"[ERROR] {string}")


def warn(string):
    if ServerConstants.DEBUG_MODE:
        print(f"[ERROR] {string}")
