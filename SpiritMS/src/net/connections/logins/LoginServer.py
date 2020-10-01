import socket

from src.net.client.PacketClient import WvsLoginClient
from src.net.client.SocketClient import SocketClient
from src.net.client.User import User
from src.net.debug.Debug import Debug
from threading import Thread

from src.net.login.Login import Login

"""
Simple Client to Server Communications for Logging in.
@author Brandon
Created: 8/21/2020
"""


class LoginServer:

    def __init__(self):
        self._LOW_PORT = 8484
        self._HIGH_PORT = 8989
        self._HOST = "127.0.0.1"
        self._BUFFER_SIZE = 512
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users = []

    """
        Params:
        socket.AF_INET = IPv4
        socket.SOCKET_STREAM = TCP Connection
    """

    async def bind_and_listen(self):
        self.socket_server.bind((socket.gethostbyname(self._HOST), self._LOW_PORT))
        self.socket_server.listen(10)  # max connections at 10
        print(f"[LISTENING] Listening for connections on port: {self._LOW_PORT}")
        ACCEPT_THREAD = Thread(target=await self.listen_connections())
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        self.socket_server.close()

    async def listen_connections(self):
        siv = [70, 114, 30, 92]
        riv = [82, 48, 25, 115]
        while True:
            # Listen for connections
            try:
                client, address = self.socket_server.accept()
                client_socket = SocketClient(socket=client, riv=riv, siv=siv)
                maple_client = await self.on_connection(client_socket)
                print(f"[CONNECTION] {address} has connected to the server")
                await maple_client.initialize()
            except Exception as e:
                Debug.error(e)
                break

    async def on_connection(self, sock):
        maple_client = await self.client_connect(sock)
        return maple_client

    async def client_connect(self, client):
        return WvsLoginClient(self, socket=client)

    def get_users(self):
        return self.users

