from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.net.connections.database.database_constants import *
from src.net.enum.world_id import WorldId
from src.net.server.server_constants import SERVER_NAME, CHANNEL_AMOUNT, EVENT_MESSAGE
from src.net.world.world import World

Base = declarative_base()
db_engine = create_engine(f"mysql+mysqlconnector://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/"
                          f"{SCHEMA_NAME}")
Session = sessionmaker(bind=db_engine)

worlds = [
    World(
        world_id=WorldId.Scania.value,
        name=SERVER_NAME,
        channels_amount=CHANNEL_AMOUNT,
        world_event_msg=EVENT_MESSAGE
    )
]
