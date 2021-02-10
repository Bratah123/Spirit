from sqlalchemy import Column, Integer, String, ForeignKey

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

    async def save(self):
        pass