from sqlalchemy import Column, Integer
from sqlalchemy.orm.attributes import InstrumentedAttribute

from src.net.client.character.avatar.cosmetic_info import CosmeticInfo
from src.net.client.character.avatar.cosmetic_look import CosmeticLook
from src.net.client.character.character_stat import CharacterStat
from src.net.constant.item_constants import is_equip
from src.net.server import global_states
from src.net.util import wz_reader


class Character(global_states.Base):
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

    __tablename__ = "characters"

    _id = Column("id", Integer, primary_key=True)
    _acc_id = Column("accid", Integer)
    _cosmetic_data_id = Column("avatardata", Integer)
    _cosmetic_info = CosmeticInfo(cosmetic_id=_id)
    _ranking = None

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
            ranking=None,
    ):
        # Database attributes
        self._id = chr_id
        self._acc_id = acc_id

        # Non-Database attributes
        self._client = client

        if func_key_maps is None:
            func_key_maps = []

        self._cosmetic_info = CosmeticInfo(cosmetic_id=chr_id)

        cosmetic_look = CosmeticLook(
            gender=gender,
            skin=skin,
            face=face,
            hair=hair,
            job_id=job_id
        )
        cosmetic_look.init_in_db()

        self._cosmetic_info.cosmetic_look = cosmetic_look

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
            chr_id=chr_id,
            chr_stat_id=chr_id,
            chr_id_for_log=chr_id,
            name=name,
            job=job_id,
            sub_job=cur_selected_sub_job,
            gender=gender,
            skin=skin,
            hair=hair,
            face=face,
        )
        character_stat.init_in_db()

        self._cosmetic_info.character_stat = character_stat

        self._ranking = ranking

    @property
    def chr_id(self):
        return self._id

    @property
    def cosmetic_info(self):
        return self._cosmetic_info

    @property
    def ranking(self):
        return self._ranking

    def init_avatar_data(self):
        self.cosmetic_info.cosmetic_look = self.get_cosmetic_look_from_db()
        self.cosmetic_info.character_stat = self.get_chr_stat_from_db()

    def get_chr_stat_from_db(self):
        session = global_states.Session()
        char_stat = session.query(CharacterStat).filter(CharacterStat._chr_id == self.chr_id).scalar()
        session.expunge_all()
        session.close()
        return char_stat

    def get_cosmetic_look_from_db(self):
        session = global_states.Session()
        cosmetic_look = session.query(CosmeticLook).filter(CosmeticLook._id == self.chr_id).scalar()
        session.expunge_all()
        session.close()
        return cosmetic_look

    async def init_in_db(self):
        """
        This function should only be used for newly created characters NOT FOR SAVING
        Returns
        -------

        """
        session = global_states.Session()
        session.add(self)
        session.commit()
        session.expunge_all()
        session.close()

    async def save(self):
        session = global_states.Session()
        mapped_values = {}

        for item in Character.__dict__.items():
            field_name = item[0]
            field_type = item[1]
            is_column = isinstance(field_type, InstrumentedAttribute)
            if is_column:
                mapped_values[field_name] = getattr(self, field_name)

        session.query(CosmeticLook).filter(Character._id == self.chr_id).update(mapped_values)
        session.commit()
        session.close()

        await self.cosmetic_info.cosmetic_look.save()
        await self.cosmetic_info.character_stat.save()

    async def save_all(self):
        pass
