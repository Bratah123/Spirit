from src.net.enum.world_id import WorldId
from src.net.server.server_constants import SERVER_NAME, CHANNEL_AMOUNT, EVENT_MESSAGE
from src.net.world.world import World

worlds = [
    World(
        world_id=WorldId.Scania.value,
        name=SERVER_NAME,
        channels_amount=CHANNEL_AMOUNT,
        world_event_msg=EVENT_MESSAGE
    )
]