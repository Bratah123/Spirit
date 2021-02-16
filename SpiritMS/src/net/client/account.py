from sqlalchemy import Column, Integer, String, ForeignKey

from src.net.client.character.character import Character
from src.net.server import global_states
from src.net.server.global_states import Base


class Account(Base):
    """
    Represents an Account in MapleStory. Not World-Wide though (Scania, Bera).
    Every User will be assigned a different "account" for each world
    """

    __tablename__ = "accounts"

    _id = Column("id", Integer, primary_key=True)
    _world_id = Column("worldid", Integer)
    _user_id = Column("userid", Integer)
    _nx_credit = Column("nxCredit", Integer)

    _characters = []

    _trunk = None
    _employee_trunk = None

    _friends = []

    _user = None
    _current_chr = None

    def __init__(
            self,
            user=None,
            world_id=0
    ):
        self._id = 0
        self._world_id = world_id
        self._user_id = user.user_id
        self._nx_credit = 0

        self._characters = []

        self._trunk = None
        self._employee_trunk = None

        self._friends = []

        self._user = user
        self._current_chr = None

    @property
    def account_id(self):
        return self._id

    @account_id.setter
    def account_id(self, value):
        self._id = value

    @property
    def world_id(self):
        return self._world_id

    @property
    def user_id(self):
        return self._user_id

    @property
    def characters(self):
        return self._characters

    @property
    def user(self):
        return self._user

    @property
    def current_chr(self):
        return self._current_chr

    @property
    def trunk(self):
        return self._trunk

    @trunk.setter
    def trunk(self, new_trunk):
        self._trunk = new_trunk

    def get_char_by_id(self, chr_id):
        chr_id = int(chr_id)
        for char in self.characters:
            if char.chr_id == chr_id:
                return char
        return None

    def init_characters(self):
        """
        Adds all characters from this account into characters list (checks db)
        Returns: void
        -------

        """
        session = global_states.Session()
        characters = session.query(Character).filter(Character._acc_id == self.account_id).all()
        for char in characters:
            char.init_avatar_data()
            self.characters.append(char)
        session.expunge_all()
        session.close()

    async def save(self):
        pass
