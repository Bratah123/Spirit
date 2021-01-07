"""
Static "class"
@author Brandon
Created: 8/21/2020
"""

from src.net.packets.send_ops import OutPacket
from src.net.packets.byte_buffer.packet import Packet
from src.net.server import server_constants


class Login:

    @staticmethod
    def send_connect(siv, riv):

        send_packet = Packet(opcode=15)

        send_packet.encode_short(server_constants.SERVER_VERSION)
        send_packet.encode_string(server_constants.MINOR_VERSION)
        send_packet.encode_int(riv)
        send_packet.encode_int(siv)
        send_packet.encode_byte(server_constants.LOCALE)
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

        send_packet.encode_byte(False)  # encode byte

        return send_packet

    @staticmethod
    def send_auth_response(response):
        send_packet = Packet(OutPacket.PRIVATE_SERVER_PACKET.value)

        send_packet.encode_int(response)

        return send_packet
