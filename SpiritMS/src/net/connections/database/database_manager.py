from swordie_db.database import SwordieDB

from src.net.client.account import Account
from src.net.connections.database.database_constants import *
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


async def register_user(username, password):
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
            f"INSERT INTO users (name, password, accounttype, characterslots) VALUES " +
            f"('{username}', '{password}', {AccountType.Player.value}, 4)"
        )
        con.commit()
        con.disconnect()
        return True
    except Exception as e:
        print("[ERROR] Error trying to register account", e)
        return False


async def create_account(account: Account):
    """This creates a new row "Account" object into the database"""
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
            f"INSERT INTO accounts (worldid, userid) VALUES " +
            f"({account.world_id}, {account.user_id})"
        )
        con.commit()
        con.disconnect()
        debug.logs(f"Successfully created account object in DB userid: {account.user_id}")
        return True
    except Exception as e:
        print("[ERROR] Error trying to create new account", e)
        return False


async def get_next_available_chr_id():
    """Checks database for the next character id that isn't taken"""
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
            "SELECT id FROM `characters` ORDER BY `id` DESC LIMIT 1"
        )
        rows = cursor.fetchall()
        biggest_id = rows[0]
        con.disconnect()
        if len(rows) < 1:
            return 1
        return int(biggest_id['id']) + 1
    except Exception as e:
        print("[ERROR] Error trying to get next character id in Database", e)
        return 1


async def get_next_available_acc_id():
    """Checks database for the next character id that isn't taken"""
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
            "SELECT id FROM `accounts` ORDER BY `id` DESC LIMIT 1"
        )
        rows = cursor.fetchall()
        biggest_id = rows[0]
        con.disconnect()
        if len(rows) < 1:
            return 1
        return int(biggest_id['id']) + 1
    except Exception as e:
        print("[ERROR] Error trying to get next character id in Database", e)
        return None
