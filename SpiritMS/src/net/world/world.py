from src.net.server import server_constants


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

        self._parties = {}
        self._guilds = {}
        self._alliances = {}
        self._connect_chat_clients = {}

        self._char_create_block = False
        self._reboot = reboot
