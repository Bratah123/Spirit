import socket
from asyncio import get_event_loop, create_task
from random import randint

from src.net.client.PacketClient import WvsLoginClient
from src.net.client.SocketClient import SocketClient
from src.net.client.User import User
from src.net.debug.Debug import Debug
from threading import Thread

from src.net.handlers.PacketHandler import PacketHandler, packet_handler
from src.net.login.Login import Login
from src.net.packets.InPackets import InPacket
from src.net.packets.encryption.MapleIV import MapleIV
from src.net.server import ServerConstants

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
        self._loop = get_event_loop()
        self._packet_handlers = []

        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setblocking(0)
        self.socket_server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.users = []

        self.add_packet_handlers()

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
        siv = MapleIV(randint(0, 2 ** 31 - 1))
        riv = MapleIV(randint(0, 2 ** 31 - 1))
        while True:
            # Listen for connections
            try:
                client, address = await self._loop.sock_accept(self.socket_server)
                client.setblocking(0)
                client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                user = User(client)
                self.users.append(user)
                client_socket = SocketClient(socket=client, riv=riv, siv=siv)
                maple_client = await self.on_connection(client_socket)
                print(f"[CONNECTION] {address} has connected to the server")
                await maple_client.initialize()
            except Exception as e:
                Debug.error(e)
                break

    async def on_connection(self, sock):
        maple_client = await getattr(self, 'client_connect')(sock)
        return maple_client

    async def client_connect(self, client):
        return WvsLoginClient(self, socket=client)

    def add_packet_handlers(self):
        import inspect

        members = inspect.getmembers(self)
        for _, member in members:
            # register all packet handlers for server

            if isinstance(member, PacketHandler) and member not in self._packet_handlers:
                self._packet_handlers.append(member)

    def get_users(self):
        return self.users

    # TODO: Add a function that handles clients disconnecting
