"""
Static "class"
@author Brandon
Created: 8/21/2020
"""

from src.net.packets.OutPackets import OutPacket
from src.net.packets.OutPacketRecv import OutPacketRecv
from src.net.server import ServerConstants


class Login:

    @staticmethod
    def send_connect(siv, riv):
        """

        :param siv: byte[]
        :param riv: byte[]
        :return: OutPacketRecv
        """
        send_packet = OutPacketRecv()

        send_packet.encode_value(15)  # encode short
        send_packet.encode_value(ServerConstants.SERVER_VERSION)  # encode short
        send_packet.encode_string(ServerConstants.MINOR_VERSION)
        send_packet.encode_value(siv)  # encoding arrays
        send_packet.encode_value(riv)  # encoding arrays
        send_packet.encode_value(ServerConstants.LOCALE)
        send_packet.encode_value(bytes(False))  # encode byte

        return send_packet

    @staticmethod
    def send_auth_server(use_auth_server):
        """
        :param use_auth_server: boolean
        :return: OutPacketRecv
        """
        send_packet = OutPacketRecv(OutPacket.AUTH_SERVER.value)

        send_packet.encode_value(bytes(use_auth_server))

        return send_packet

    @staticmethod
    def send_start_client():
        send_packet = OutPacketRecv(OutPacket.CLIENT_START.value)

        send_packet.encode_value(bytes(True))  # encode byte

        return send_packet

    @staticmethod
    def send_auth_response(response):
        send_packet = OutPacketRecv(OutPacket.PRIVATE_SERVER_PACKET.value)

        send_packet.encode_value(response)

        return send_packet
