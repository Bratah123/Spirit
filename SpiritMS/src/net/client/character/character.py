from src.net.client.character.avatar.cosmetic_info import CosmeticInfo
from src.net.client.character.avatar.cosmetic_look import CosmeticLook


class Character:
    def __init__(
            self,
            id=0,
            acc_id=0,
            client=None,
            func_key_maps=None,
            user=None,
            character_stat=None,
            gender=0,
            skin=0,
            face=0,
            hair=0,
            cur_selected_sub_job=0,
            items=None,
    ):
        # Database attributes
        self._id = id
        self._acc_id = acc_id

        # Non-Database attributes
        self._client = client

        if func_key_maps is None:
            func_key_maps = []

        self._cosmetic_info = CosmeticInfo()
        self._cosmetic_info.cosmetic_look = CosmeticLook(
            gender=gender,
            skin=skin,
            face=face,
            hair=hair
        )
        hair_equips = []
        for item_id in items:
            pass

        self._func_key_maps = func_key_maps
        self._user = user
        self._character_stat = character_stat

    @property
    def id(self):
        return self._id
