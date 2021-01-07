from src.net.server import server_constants


class Debug:
    @staticmethod
    def logs(string):
        if server_constants.DEBUG_MODE:
            print(f"[DEBUG] {string}")

    @staticmethod
    def error(string):
        if server_constants.DEBUG_MODE:
            print(f"[ERROR] {string}")

    @staticmethod
    def warn(string):
        if server_constants.DEBUG_MODE:
            print(f"[ERROR] {string}")
