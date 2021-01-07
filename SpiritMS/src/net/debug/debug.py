from src.net.server import server_constants


def logs(string):
    if server_constants.DEBUG_MODE:
        print(f"[DEBUG] {string}")


def error(string):
    if server_constants.DEBUG_MODE:
        print(f"[ERROR] {string}")


def warn(string):
    if server_constants.DEBUG_MODE:
        print(f"[ERROR] {string}")
