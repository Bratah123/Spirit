from src.net.client.packet_client import WvsLoginClient
from src.net.handlers.packet_handler import packet_handler
from src.net.packets.recv_ops import InPacket
from src.net.server import server_constants
from src.net.server.server_base import ServerBase
from src.net.server.server_constants import LOGIN_PORT

"""
Simple Client to Server Communications for Logging in.
@author Brandon
Created: 8/21/2020
"""


class LoginServer(ServerBase):

    def __init__(self, parent):
        super().__init__(parent, LOGIN_PORT, 'LoginServer')
        self._worlds = []

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

    @packet_handler(opcode=InPacket.PERMISSION_REQUEST)
    async def handle_permission_request(self, client, packet):
        locale = packet.decode_byte()
        version = packet.decode_short()
        minor_version = packet.decode_string()
        if locale != server_constants.LOCALE or version != server_constants.SERVER_VERSION:
            await client.close()
