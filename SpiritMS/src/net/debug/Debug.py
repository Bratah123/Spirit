from src.net.server import ServerConstants


class Debug:
    @staticmethod
    def logs(string):
        if ServerConstants.DEBUG_MODE:
            print(f"[DEBUG] {string}")

    @staticmethod
    def error(string):
        if ServerConstants.DEBUG_MODE:
            print(f"[ERROR] {string}")

    @staticmethod
    def warn(string):
        if ServerConstants.DEBUG_MODE:
            print(f"[ERROR] {string}")
