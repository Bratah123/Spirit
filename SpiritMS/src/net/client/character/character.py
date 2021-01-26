from src.net.client.character.avatar.cosmetic_info import CosmeticInfo
from src.net.client.character.avatar.cosmetic_look import CosmeticLook
from src.net.client.character.character_stat import CharacterStat


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
            name="",
            chr_id=0,
            acc_id=0,
            client=None,
            func_key_maps=None,
            user=None,
            gender=0,
            skin=0,
            face=0,
            hair=0,
            cur_selected_sub_job=0,
            items=None,
            key_setting_type=0,
            job_id=0,
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
            hair=hair,
        )

        hair_equips = []

        for item_id in items:
            pass

        self._func_key_maps = func_key_maps
        self._user = user

        character_stat = CharacterStat(  # see character_stat.py for default spawning stats
            name=name,
            job=job_id,
            sub_job=cur_selected_sub_job,
            gender=gender,
            skin=skin,
            hair=hair,
        )

        self._cosmetic_info.character_stat = character_stat

    @property
    def chr_id(self):
        return self._id

    @property
    def cosmetic_info(self):
        return self._cosmetic_info

    async def init_in_db(self):
        """
        This function should only be used for newly created characters NOT FOR SAVING
        Returns
        -------

        """
        pass

    async def save(self):
        pass

    async def save_all(self):
        pass
