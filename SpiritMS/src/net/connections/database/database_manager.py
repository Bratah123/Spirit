from swordie_db.database import SwordieDB

from src.net.connections.database.database_constants import SCHEMA_NAME
from src.net.debug import debug


async def get_user_from_db(username):
    spirit = SwordieDB(schema=SCHEMA_NAME)
    try:
        user = spirit.get_user_by_username(username)
        return user
    except Exception as e:
        debug.error(e)
        return None
