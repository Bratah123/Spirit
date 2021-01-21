from src.net.server import server_constants
from src.net.world.channel import Channel


class World:
    # World Struct
    def __init__(
            self,
            world_id=0,
            name=server_constants.SERVER_NAME,
            world_state=0,
            world_event_msg="",
            world_event_exp_wse=100,
            world_event_drop_wse=100,
            boom_up_event_notice=0,
            channels_amount=0,
            star_planet=False,
            reboot=False,
    ):
        self._world_id = world_id
        self._world_state = world_state
        self._world_event_exp_wse = world_event_exp_wse
        self._world_event_drop_wse = world_event_drop_wse
        self._boom_up_event_notice = boom_up_event_notice

        self._star_planet = star_planet

        self._name = name
        self._world_event_description = world_event_msg

        self._channels = []

        for i in range(1, channels_amount + 1):
            self._channels.append(
                Channel(
                    name=name,
                    world_id=world_id,
                    channel_id=i,
                )
            )

        self._parties = {}
        self._guilds = {}
        self._alliances = {}
        self._connect_chat_clients = {}

        self._char_create_block = False
        self._reboot = reboot

    @property
    def world_id(self):
        return self._world_id

    @property
    def world_state(self):
        return self._world_state

    @property
    def world_event_exp_wse(self):
        return self._world_event_exp_wse

    @property
    def world_event_drop_wse(self):
        return self._world_event_drop_wse

    @property
    def boom_up_event_notice(self):
        return self._boom_up_event_notice

    @property
    def star_planet(self):
        return self._star_planet

    @property
    def name(self):
        return self._name

    @property
    def world_event_description(self):
        return self._world_event_description

    @property
    def char_create_block(self):
        return self._char_create_block

    @property
    def reboot(self):
        return self._reboot

    @property
    def channels(self):
        return self._channels

    def get_channel_size(self):
        return len(self.channels)

    def is_full(self):
        full = True
        for channel in self.channels:
            if channel.get_size() < channel.max_size:
                full = False
                break
        return full

    def get_channel_by_id(self, channel_id):
        for channel in self.channels:
            if channel.channel_id == channel_id:
                return channel
        return None
