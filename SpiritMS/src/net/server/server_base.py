from asyncio import get_event_loop, create_task, Event, Task
from src.net.debug import debug

from src.net.client.socket_client import SocketClient
from src.net.handlers.packet_handler import PacketHandler
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
        self._dispatcher = PacketReader(self)

        self.add_packet_handlers()

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

    def add_packet_handlers(self):
        import inspect

        members = inspect.getmembers(self)
        for _, member in members:
            # register all packet handlers for server

            if isinstance(member, PacketHandler) and member not in self._packet_handlers:
                self._packet_handlers.append(member)

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
    def dispatcher(self):
        return self._dispatcher

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