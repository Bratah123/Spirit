from src.net.debug.Debug import Debug


class PacketClient:
    def __init__(self, parent, socket):
        self.socket = socket
        self._parent = parent
        self._port = None
        self._is_online = False

        self.logged_in = False
        self.world_id = None
        self.channel_id = None

    async def send_packet(self, packet):
        Debug.logs(packet.to_string())
        await self.socket.send_packet(packet)

    async def send_packet_raw(self, packet):
        Debug.logs(packet.to_string())
        await self.socket.send_packet_raw(packet)

    @property
    def parent(self):
        return self._parent

    @property
    def get_ip(self):
        return self.socket.identifier[0]

    @property
    def get_data(self):
        return self._parent.data