from swordie_db.database import SwordieDB

from src.net.connections.database.database_constants import SCHEMA_NAME
from src.net.debug import debug
import mysql.connector

from src.net.enum.account_type import AccountType

"""
    Please keep all database functions async - Brandon
"""


async def get_user_from_db(username):
    spirit = SwordieDB(schema=SCHEMA_NAME)
    try:
        user = spirit.get_user_by_username(username)
        return user
    except Exception as e:
        debug.error(e)
        return None


async def check_name_taken(name):
    spirit = SwordieDB(schema=SCHEMA_NAME)
    try:
        spirit.get_char_by_name(name)
    except Exception:
        return False
    return True


async def register_account(username, password):
    try:
        con = mysql.connector.connect(database=SCHEMA_NAME)
        cursor = con.cursor(dictionary=True)
        cursor.execute(
            f"INSERT INTO users (name, password, accounttype, characterslots VALUES " +
            f"{username}, {password}, {AccountType.Player.value}, 4"
        )
        con.commit()
        con.disconnect()
        return True
    except Exception as e:
        print("[ERROR] Error trying to register account", e)
        return False
