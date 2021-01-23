from src.net.client.character.avatar.cosmetic_info import CosmeticInfo
from src.net.client.character.avatar.cosmetic_look import CosmeticLook


class Character:
    """
    The Character class a representation of a MapleStory "character"
    Notable attributes:
        character_stat:
            class CharacterStat
            Stores every stat in MapleStory (I.E. HP, MP, DEX, STR, MESOS)
        cosmetic_info:
            class CosmeticInfo:
            You guessed it, this attribute stores all of the characters cosmetic related stats.
            (I.E. HAIR, FACE, EYE)
    """
    def __init__(
            self,
            chr_id=0,
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
        self._id = chr_id
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
    def chr_id(self):
        return self._id

    async def save(self):
        pass

    async def save_all(self):
        pass