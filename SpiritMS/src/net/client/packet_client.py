from src.net.debug import debug
from src.net.packets.byte_buffer.packet import Packet
from src.net.packets.send_ops import OutPacket
from src.net.server import server_constants


class PacketClient:
    def __init__(self, parent, socket):
        self.socket = socket
        self._parent = parent
        self._port = None
        self._is_online = False

        self.logged_in = False
        self.world_id = None
        self.channel_id = None

    async def initialize(self):
        # Handshake packet
        send_packet = Packet(opcode=15)

        send_packet.encode_short(server_constants.SERVER_VERSION)
        send_packet.encode_string(server_constants.MINOR_VERSION)
        send_packet.encode_int(self.socket.riv.value)
        send_packet.encode_int(self.socket.siv.value)
        send_packet.encode_byte(server_constants.LOCALE)
        send_packet.encode_byte(False)

        await self.send_packet_raw(send_packet)

        await self.receive()

    async def receive(self):
        await self.socket.receive(self)

    def dispatch(self, packet):
        self._parent.packet_reader.push(self, packet)

    async def send_packet(self, packet):
        debug.logs("OutPacket Opcode: " + str(packet.name) + " | " + str(packet.to_string()) + " |")
        await self.socket.send_packet(packet)

    async def send_packet_raw(self, packet):
        debug.logs("OutPacket Opcode: " + str(packet.name) + " | " + str(packet.to_string()) + " |")
        await self.socket.send_packet_raw(packet)

    @property
    def parent(self):
        return self._parent

    @property
    def ip(self):
        return self.socket.identifier[0]

    @property
    def data(self):
        return self._parent.data


class WvsLoginClient(PacketClient):
    def __init__(self, parent, socket):
        super().__init__(parent, socket)

        self._account = None
        self._user = None
        self._world_id = 0
        self._channel = 0
        self.avatars = []

    def close(self):
        self.socket.close()

    @property
    def account_id(self):
        return self.account.id if getattr(self.account, 'id') else - 1

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user_obj):
        self._user = user_obj

    @property
    def account(self):
        return self._account

    @account.setter
    def account(self, account_obj):
        self._account = account_obj

    @property
    def world_id(self):
        return self._world_id

    @world_id.setter
    def world_id(self, wid):
        self._world_id = wid

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, new_channel):
        self._channel = new_channel
