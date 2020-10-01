"""
Static "class"
@author Brandon
Created: 8/21/2020
"""

from src.net.packets.OutPackets import OutPacket
from src.net.packets.byte_buffer.Packet import Packet
from src.net.server import ServerConstants


class Login:

    @staticmethod
    def send_connect(siv, riv):

        send_packet = Packet(opcode=15)

        send_packet.encode_short(ServerConstants.SERVER_VERSION)
        send_packet.encode_string(ServerConstants.MINOR_VERSION)
        send_packet.encode_int(riv)
        send_packet.encode_int(siv)
        send_packet.encode_byte(ServerConstants.LOCALE)
        send_packet.encode_byte(False)  # encode byte

        return send_packet

    @staticmethod
    def send_auth_server(use_auth_server):
        """
        :param use_auth_server: boolean
        :return: OutPacketRecv
        """
        send_packet = Packet(OutPacket.AUTH_SERVER.value)

        send_packet.encode_byte(use_auth_server)

        return send_packet

    @staticmethod
    def send_start_client():
        send_packet = Packet(OutPacket.CLIENT_START.value)

        send_packet.encode_value(True)  # encode byte

        return send_packet

    @staticmethod
    def send_auth_response(response):
        send_packet = Packet(OutPacket.PRIVATE_SERVER_PACKET.value)

        send_packet.encode_int(response)

        return send_packet
