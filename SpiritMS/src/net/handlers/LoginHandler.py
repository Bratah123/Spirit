from src.net.connections.logins.LoginServer import LoginServer
from src.net.handlers.PacketHandler import packet_handler
from src.net.login.Login import Login
from src.net.packets.InPackets import InPacket
from src.net.server import ServerConstants


class LoginHandler:

    @packet_handler(opcode=InPacket.PERMISSION_REQUEST)
    def handle_permission_request(self, client, packet):
        locale = packet.decode_byte()
        version = packet.decode_short()
        minor_version = packet.decode_string()
        if locale != ServerConstants.LOCALE or version != ServerConstants.SERVER_VERSION:
            client.close()

    @packet_handler(opcode=InPacket.USE_AUTH_SERVER)
    def handle_auth_server(self, client, packet):
        await client.send_packet(Login.send_auth_server(False))

    @packet_handler(opcode=InPacket.CLIENT_START)
    def handle_client_start(self, client, packet):
        await client.send_packet(Login.send_start_client())