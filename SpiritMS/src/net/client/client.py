from random import randint

from src.net.client.socket_client import SocketClient
from src.net.packets.encryption.maple_iv import MapleIV


class Client(SocketClient):
    def __init__(self, socket, siv=MapleIV(randint(0, 2 ** 31 - 1)), riv=MapleIV(randint(0, 2 ** 31 - 1))):
        super().__init__(socket, riv, siv)
        self._siv = siv
        self._riv = riv

    def write(self, by):
        self.write(by)
