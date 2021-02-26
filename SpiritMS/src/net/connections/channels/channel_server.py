import inspect

from src.net.client.packet_client import WvsLoginClient
from src.net.handlers.packet_handler import PacketHandler
from src.net.handlers.user.migration_handler import MigrationHandler
from src.net.server.server_base import ServerBase


class ChannelServer(ServerBase):
    def __init__(self, parent, port, world_id, channel_id):
        super().__init__(parent, port, f"ChannelServer: {channel_id}")
        self._world_id = world_id
        self._channel_id = channel_id

        # Add packet handler classes here
        self._handlers = [
            MigrationHandler()
        ]

        self._exp_rate = 6
        self._drop_rate = 2
        self._meso_rate = 1

        self.add_packet_handlers()

    @property
    def parent(self):
        return self._parent

    @classmethod
    async def run(cls, parent, port, world_id, channel_id):
        channel_server = ChannelServer(parent, port, world_id, channel_id)
        await channel_server.start()

    async def client_connect(self, client):
        game_client = WvsLoginClient(self, client)
        self.parent.clients.append(game_client)

        return game_client

    def add_packet_handlers(self):
        for handler in self._handlers:
            members = inspect.getmembers(handler)
            for _, member in members:
                # register all packet handlers for server

                if isinstance(member, PacketHandler) and member not in self._packet_handlers:
                    self._packet_handlers.append(member)
