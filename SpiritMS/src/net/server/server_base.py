from asyncio import get_event_loop, Event

from src.net.client.socket_client import SocketClient
from src.net.debug import debug
from src.net.packets.packet_reader import PacketReader
from src.net.server.client_listener import ClientListener
from src.net.server.server_constants import HOST_IP


class ServerBase:
    """Server base for center, channel, and login servers

    Attributes
    -----------
    is_alive : bool
        Server alive status
    name: str
        Server specific name

    """

    def __init__(self, parent, port, name=""):
        self._loop = get_event_loop()
        self._parent = parent
        self._port = port
        self._name = name
        self._ready = Event(loop=self._loop)
        self.is_alive = False
        self._clients = []
        self._packet_handlers = []
        self._packet_reader = PacketReader(self)

    @property
    def clients(self):
        return self._clients

    async def start(self):
        self.is_alive = True
        self._acceptor = ClientListener(self, (HOST_IP, self._port))

        self._ready.set()
        self._listener = self._loop.create_task(self.listen())

    def close(self):
        self._listener.cancel()

    async def on_client_accepted(self, socket):
        client = SocketClient(socket=socket)
        maple_client = await getattr(self, 'client_connect')(client)

        debug.logs(f"{self.name} Connection Accepted at {maple_client.ip}")

        self._clients.append(maple_client)
        await maple_client.initialize()

    def on_client_disconnect(self, client):
        self._clients.remove(client)

        debug.logs(f"Client Disconnected {client.ip}")

    async def wait_until_ready(self):
        """|coro|

        Waits until the GameServer has started listening for clients.
        """
        await self._ready.wait()

    def listen(self):
        return self._acceptor._listen()

    @property
    def data(self):
        return self._parent.data

    @property
    def packet_reader(self):
        return self._packet_reader

    @property
    def name(self):
        return self._name

    @property
    def parent(self):
        return self._parent

    @property
    def port(self):
        return self._port

    @property
    def population(self):
        return len(self._clients)

    @property
    def packet_handlers(self):
        return self._packet_handlers
