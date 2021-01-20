from src.net.client.packet_client import WvsLoginClient
from src.net.handlers.login_handler import LoginHandler
from src.net.handlers.packet_handler import PacketHandler
from src.net.server.server_base import ServerBase
from src.net.server.server_constants import LOGIN_PORT
import inspect

"""
Simple Client to Server Communications for Logging in.
@author Brandon
Created: 8/21/2020
"""


class LoginServer(ServerBase):

    def __init__(self, parent):
        super().__init__(parent, LOGIN_PORT, 'LoginServer')
        self._worlds = []
        self._handlers = [
            LoginHandler()
        ]

        self.add_packet_handlers()

    """
        Params:
        socket.AF_INET = IPv4
        socket.SOCKET_STREAM = TCP Connection
    """

    def add_world(self, world):
        self._worlds.append(world)

    @classmethod
    async def run(cls, parent):
        login_server = LoginServer(parent)
        await login_server.start()

    async def client_connect(self, client):
        return WvsLoginClient(self, client)

    def add_packet_handlers(self):
        for handler in self._handlers:
            members = inspect.getmembers(handler)
            for _, member in members:
                # register all packet handlers for server

                if isinstance(member, PacketHandler) and member not in self._packet_handlers:
                    self._packet_handlers.append(member)
