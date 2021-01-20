from src.net.packets.byte_buffer.packet import Packet
from src.net.packets.send_ops import OutPacket


class WvsContext:

    @staticmethod
    def broadcast_msg(broadcast_msg):
        send_packet = Packet(opcode=OutPacket.BROADCAST_MSG)

        broadcast_msg.encode(send_packet)

        return send_packet
