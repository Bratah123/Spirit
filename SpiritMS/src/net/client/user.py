import mysql.connector
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm.attributes import InstrumentedAttribute

from src.net.client.account import Account
from src.net.connections.database.database_constants import *
from src.net.enum import account_type
from src.net.enum.pic_status import PicStatus
from src.net.server import global_states


class User(global_states.Base):
    """This class is a representation of an "Account" in MapleStory
    However, the User Class represents all attributes of an account regardless of World (Scania, ETC)
    Params:
        client: Client
    """
    __tablename__ = "users"

    _id = Column("id", Integer, primary_key=True)
    _name = Column("name", String)
    _password = Column("password", String)
    _pic = Column("pic", String)
    _account_type = Column("accounttype", Integer)
    _vote_point = Column("votepoints", Integer)
    _donation_points = Column("donationpoints", Integer)
    _age = Column("age", Integer)
    _vip_grade = Column("vipgrade", Integer)
    _block_reason = Column("nblockreason", Integer)
    _gender = Column("gender", Integer)
    _msg2 = Column("msg2", Integer)
    _purchase_exp = Column("purchaseexp", Integer)
    _p_block_reason = Column("pblockreason", Integer)
    _grade_code = Column("gradecode", Integer)
    _chat_unblock_date = Column("chatunblockdate", Integer)
    _has_censored_nx_login_id = Column("hascensorednxloginid", Integer)
    _censored_nx_login_id = Column("censorednxloginid", String)
    _character_slots = Column("characterslots", Integer)
    _creation_date = Column("creationdate", String)
    _maple_points = Column("maplePoints", Integer)
    _nx_prepaid = Column("nxPrepaid", Integer)
    _ban_reason = Column("banreason", String)

    _current_chr = None
    _current_account = None

    _accounts = []

    def __init__(
            self,
            user_id=0,
            name="",
            password="",
            pic="",
            acc_type=None,
            vote_point=0,
            donation_points=0,
            age=0,
            vip_grade=0,
            block_reason=0,
            gender=0,
            msg2=0,
            purchase_exp=0,
            p_block_reason=0,
            grade_code=0,
            chat_unblock_date=0,
            has_censored_nx_login_id=0,
            censored_nx_login_id="",
            character_slots=4,
            creation_date=None,
            maple_points=0,
            nx_prepaid=0,
            ban_reason=""
    ):
        self._id = user_id
        self._name = name
        self._password = password
        self._pic = pic
        self._account_type = acc_type
        self._vote_point = vote_point
        self._donation_points = donation_points
        self._age = age
        self._vip_grade = vip_grade
        self._block_reason = block_reason
        self._gender = gender
        self._msg2 = msg2
        self._purchase_exp = purchase_exp
        self._p_block_reason = p_block_reason
        self._grade_code = grade_code
        self._chat_unblock_date = chat_unblock_date
        self._has_censored_nx_login_id = has_censored_nx_login_id
        self._censored_nx_login_id = censored_nx_login_id
        self._character_slots = character_slots
        self._creation_date = creation_date
        self._maple_points = maple_points
        self._nx_prepaid = nx_prepaid
        self._ban_reason = ban_reason

        self._current_chr = None
        self._current_account = None

        self._accounts = []

    @staticmethod
    async def get_user_from_name(username: str):
        """

        Parameters
        ----------
        username: username aka "name" in database

        Returns User (itself)
        -------

        """

        session = global_states.Session()
        user = session.query(User).filter(User._name == username).scalar()
        session.close()

        return user

    @property
    def user_id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def password(self):
        return self._password

    @property
    def pic(self):
        return self._pic

    @property
    def acc_type(self):
        # Return the Enum AccountType rather than the int
        acc_type_string = ""
        if self._account_type == 4:
            acc_type_string = "Admin"
        elif self._account_type == 0:
            acc_type_string = "Player"
        elif self._account_type == 3:
            acc_type_string = "Intern"
        elif self._account_type == 5:
            acc_type_string = "Tester"

        return account_type.get_account_type_by_name(acc_type_string)

    @property
    def vote_points(self):
        return self._vote_point

    @property
    def donation_points(self):
        return self._donation_points

    @property
    def age(self):
        return self._age

    @property
    def vip_grade(self):
        return self._vip_grade

    @property
    def block_reason(self):
        return self._block_reason

    @property
    def gender(self):
        return self._gender

    @property
    def msg2(self):
        return self._msg2

    @property
    def purchase_exp(self):
        return self._purchase_exp

    @property
    def p_block_reason(self):
        return self._p_block_reason

    @property
    def grade_code(self):
        return self._grade_code

    @property
    def has_censored_nx_login_id(self):
        return self._has_censored_nx_login_id

    @property
    def character_slots(self):
        return self._character_slots

    @property
    def maple_points(self):
        return self._maple_points

    @property
    def nx_prepaid(self):
        return self._nx_prepaid

    @property
    def current_chr(self):
        return self._current_chr

    @property
    def censored_nx_login_id(self):
        return self._censored_nx_login_id

    @property
    def chat_unblock_date(self):
        return self._chat_unblock_date

    @property
    def creation_date(self):
        return self._creation_date

    @property
    def accounts(self):
        return self._accounts

    async def save(self):
        session = global_states.Session()
        mapped_values = {}

        for item in User.__dict__.items():
            field_name = item[0]
            field_type = item[1]
            is_column = isinstance(field_type, InstrumentedAttribute)
            if is_column:
                mapped_values[field_name] = getattr(self, field_name)

        session.query(User).filter(User._id == self.user_id).update(mapped_values)
        session.commit()
        session.close()

    def get_account_by_world_id(self, world_id):
        for account in self.accounts:
            if account.world_id == world_id:
                return account
        return None

    def add_account(self, account):
        self._accounts.append(account)

    def get_pic_status(self):
        pic_status = None
        if self.pic is None or len(self.pic) <= 0:
            pic_status = PicStatus.CREATE_PIC
        else:
            pic_status = PicStatus.ENTER_PIC

        return pic_status

    def get_account_from_db(self):
        session = global_states.Session()
        account = session.query(Account).filter(Account._user_id == self.user_id).scalar()
        session.close()
        if account is not None:
            account.init_characters()
        return account
