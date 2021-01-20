from src.net.debug import debug
from src.net.login.login import Login
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
        send_packet = Packet(opcode=15)

        send_packet.encode_short(server_constants.SERVER_VERSION)
        send_packet.encode_string(server_constants.MINOR_VERSION)
        send_packet.encode_int(self.socket.riv.value)
        send_packet.encode_int(self.socket.siv.value)
        send_packet.encode_byte(server_constants.LOCALE)
        send_packet.encode_byte(False)

        await self.send_packet_raw(send_packet)

        await self.receive()

    async def init_auth_server(self):
        send_packet = Packet(opcode=OutPacket.AUTH_SERVER)

        send_packet.encode_byte(False)

        await self.send_packet(send_packet)

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

        self.account = None
        self.avatars = []

    async def login(self, username, password):
        response, account = await self.data. \
            account(username=username, password=password).login()

        if not response:
            self.account = account
            self.logged_in = True
            return 0

        return response

    async def load_avatars(self, world_id=None):
        self.avatars = await self.data \
            .account(id=self.account.id) \
            .get_characters(world_id=world_id)

    @property
    def account_id(self):
        return self.account.id if getattr(self.account, 'id') else - 1
