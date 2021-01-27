from src.net.client.character.avatar.cosmetic_info import CosmeticInfo
from src.net.client.character.avatar.cosmetic_look import CosmeticLook
from src.net.client.character.character_stat import CharacterStat
from src.net.constant.item_constants import is_equip
from src.net.util import wz_reader


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
            job_id=job_id
        )

        hair_equips = []

        for item_id in items:
            weapon_info = wz_reader.get_weapon_info(item_id)
            if is_equip(item_id):
                hair_equips.append(item_id)
                if weapon_info is not None:
                    if weapon_info["islot"].lower() == "wp":
                        if weapon_info["cash"] == "0":
                            self._cosmetic_info.cosmetic_look.weapon_id = item_id
                        else:
                            self._cosmetic_info.cosmetic_look.weapon_sticker_id = item_id

        self._cosmetic_info.cosmetic_look.hair_equips = hair_equips

        self._func_key_maps = func_key_maps
        self._user = user

        character_stat = CharacterStat(  # see character_stat.py for default spawning stats
            name=name,
            job=job_id,
            sub_job=cur_selected_sub_job,
            gender=gender,
            skin=skin,
            hair=hair,
            face=face,
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
