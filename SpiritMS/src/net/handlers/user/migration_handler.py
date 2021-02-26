from src.net.client.packet_client import WvsLoginClient
from src.net.handlers.packet_handler import packet_handler
from src.net.packets.byte_buffer.packet import Packet
from src.net.packets.recv_ops import InPacket


class MigrationHandler:

    @packet_handler(opcode=InPacket.MIGRATE_IN)
    async def handle_migrate_in(self, client: WvsLoginClient, packet: Packet):
        pass
