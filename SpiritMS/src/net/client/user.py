import mysql.connector

from src.net.client.account import Account
from src.net.connections.database.database_constants import *
from src.net.enum import account_type
from src.net.enum.pic_status import PicStatus


class User:
    """This class is a representation of an "Account" in MapleStory
    However, the User Class represents all attributes of an account regardless of World (Scania, ETC)
    Params:
        client: Client
    """

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
            has_censored_nx_login_id="",
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
    async def get_user_from_dbuser(db_user):
        """

        Parameters
        ----------
        db_user: User class from SwordieDB

        Returns User (itself)
        -------

        """
        user_stats = db_user.user_stats
        user = User(
            user_id=user_stats['id'],
            name=user_stats['name'],
            password=db_user.password,
            pic=db_user.pic,
            acc_type=account_type.get_account_type_by_name(db_user.get_acc_type_string()),
            vote_point=db_user.vote_points,
            donation_points=db_user.donation_points,
            age=user_stats['age'],
            vip_grade=user_stats['vipgrade'],
            block_reason=user_stats['nblockreason'],
            gender=user_stats['gender'],
            msg2=user_stats['msg2'],
            purchase_exp=user_stats['purchaseexp'],
            p_block_reason=user_stats['pblockreason'],
            has_censored_nx_login_id=user_stats['hascensorednxloginid'],
            grade_code=user_stats['gradecode'],
            censored_nx_login_id=user_stats['censorednxloginid'],
            character_slots=user_stats['characterslots'],
            creation_date=user_stats['creationdate'],
            maple_points=db_user.maple_points,
            nx_prepaid=db_user.nx_prepaid,
            ban_reason=db_user.ban_reason

        )
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
        return self._account_type

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
        try:
            con = mysql.connector.connect(
                database=SCHEMA_NAME,
                host=DATABASE_HOST,
                user=DATABASE_USER,
                password=DATABASE_PASSWORD,
                port=DATABASE_PORT,
            )

            cursor = con.cursor(dictionary=True)

            cursor.execute(
                f"SELECT * FROM accounts WHERE userid = {self.user_id}"
            )
            rows = cursor.fetchall()
            con.disconnect()
            account = Account(
                user=self,
                world_id=rows[0]['worldid']  # we get the first row, cause source don't support multiple worlds
            )
            return account
        except Exception:
            return None
