import socket

from src.net.client.Client import Client
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

    def bind_and_listen(self):
        self.socket_server.bind((socket.gethostbyname(self._HOST), self._LOW_PORT))
        self.socket_server.listen(10)  # max connections at 10
        print(f"[LISTENING] Listening for connections on port: {self._LOW_PORT}")
        ACCEPT_THREAD = Thread(target=self.listen_connections())
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        self.socket_server.close()

    def listen_connections(self):
        siv = [70, 114, 30, 92]
        riv = [82, 48, 25, 115]
        while True:
            # Listen for connections
            try:
                client, address = self.socket_server.accept()
                user = User(client)
                c = Client(bytes(siv), bytes(riv))
                c.write(Login.send_connect(bytes(siv), bytes(riv)))
                self.users.append(user)
                print(f"[CONNECTION] {address} has connected to the server")
            except Exception as e:
                Debug.error(e)
                break

    def get_users(self):
        return self.users
