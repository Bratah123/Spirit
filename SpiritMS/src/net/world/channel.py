from src.net.server.server_constants import LOGIN_PORT


class Channel:
    # Channel Struct
    def __init__(
            self,
            name="",
            world_id=0,
            channel_id=1,
            adult_channel=False,
    ):
        self._name = name
        self._world_id = world_id
        self._channel_id = channel_id
        self._port = LOGIN_PORT + 100 + channel_id
        self._adult_channel = adult_channel

        self._fields = []

        self._characters = {}
        self._max_size = 10000

    @property
    def name(self):
        return self._name

    @property
    def world_id(self):
        return self._world_id

    @property
    def channel_id(self):
        return self._channel_id

    @property
    def port(self):
        return self._port

    @property
    def adult_channel(self):
        return self._adult_channel

    @property
    def characters(self):
        return self._characters

    @property
    def max_size(self):
        return self._max_size

    def get_gauge_percent(self):
        return max(1, len(self.characters) // self.max_size)
