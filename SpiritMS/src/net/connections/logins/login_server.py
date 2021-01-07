import socket
from asyncio import get_event_loop, create_task
from random import randint

from src.net.client.packet_client import WvsLoginClient
from src.net.client.socket_client import SocketClient
from src.net.client.user import User
from src.net.debug.debug import Debug
from threading import Thread

from src.net.handlers.packet_handler import PacketHandler, packet_handler
from src.net.packets.recv_ops import InPacket
from src.net.packets.packet_reader import PacketReader
from src.net.packets.encryption.maple_iv import MapleIV
from src.net.server import server_constants

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

        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setblocking(False)
        self.socket_server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.users = []
        self._packet_handlers = []
        self._packet_reader = PacketReader(self)

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
        while True:
            # Listen for connections
            try:
                siv = MapleIV(randint(0, 2 ** 31 - 1))
                riv = MapleIV(randint(0, 2 ** 31 - 1))
                client, address = await self._loop.sock_accept(self.socket_server)
                client.setblocking(False)
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
        return WvsLoginClient(parent=self, socket=client)

    def add_packet_handlers(self):
        import inspect

        members = inspect.getmembers(self)
        for _, member in members:
            # register all packet handlers for server
            if isinstance(member, PacketHandler) and member not in self._packet_handlers:
                self._packet_handlers.append(member)

    def get_users(self):
        return self.users

    @property
    def packet_reader(self):
        return self._packet_reader

    @packet_handler(opcode=InPacket.PERMISSION_REQUEST)
    async def handle_permission_request(self, client, packet):
        locale = packet.decode_byte()
        version = packet.decode_short()
        minor_version = packet.decode_string()
        if locale != server_constants.LOCALE or version != server_constants.SERVER_VERSION:
            await client.close()

    def on_client_disconnect(self, client):
        self.users.remove(client)
        print("A Client has disconnected from the server!")
