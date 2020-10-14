from src.net.client.SocketClient import SocketClient


class Client(SocketClient):
    def __init__(self, siv, riv, socket):
        super().__init__(socket, riv, siv)
        self._siv = siv
        self._riv = riv

    def write(self, by):
        self.write(by)
