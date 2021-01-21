from src.net.client.account import Account
from src.net.client.character.broadcast_msg import BroadcastMsg
from src.net.client.packet_client import WvsLoginClient
from src.net.client.user import User
from src.net.connections.database import database_manager
from src.net.connections.packet.wvs_context import WvsContext
from src.net.debug import debug
from src.net.enum.login_type import LoginType
from src.net.enum.world_id import WorldId
from src.net.handlers.packet_handler import packet_handler
from src.net.login.login import Login
from src.net.packets.byte_buffer.packet import Packet
from src.net.packets.recv_ops import InPacket
from src.net.packets.send_ops import OutPacket
from src.net.server import server_constants, global_states
from src.net.server.global_states import worlds


class LoginHandler:

    @packet_handler(opcode=InPacket.PERMISSION_REQUEST)
    async def handle_permission_request(self, client, packet):
        locale = packet.decode_byte()
        version = packet.decode_short()
        minor_version = packet.decode_string()
        if locale != server_constants.LOCALE or version != server_constants.SERVER_VERSION:
            client.close()

    @packet_handler(opcode=InPacket.USE_AUTH_SERVER)
    async def handle_auth_server(self, client, packet):
        await client.send_packet(Login.send_auth_server(False))

    @packet_handler(opcode=InPacket.CLIENT_START)
    async def handle_client_start(self, client, packet):
        await client.send_packet(Login.send_start_client())

    @packet_handler(opcode=InPacket.PRIVATE_SERVER_PACKET)
    async def handle_private_server_packet(self, client, packet):
        await client.send_packet(Login.send_auth_response(
            OutPacket.PRIVATE_SERVER_PACKET.value ^ packet.decode_int()
        ))

    @packet_handler(opcode=InPacket.CHECK_LOGIN_AUTH_INFO)
    async def handle_check_login_auth_info(self, client, packet):
        sid = packet.decode_byte()
        password = packet.decode_string()
        username = packet.decode_string()
        machine_id = packet.decode_buffer(16)

        success = False
        result = None
        # db_user is a database object, setting anything would set it in the database: SwordieDB()
        db_user = await database_manager.get_user_from_db(username)
        # this user is the User object in the source
        user = None

        if db_user is not None:
            if password.lower() == "fixme":
                await client.send_packet(
                    WvsContext.broadcast_msg(BroadcastMsg.pop_up_message("Your account is now logged out"))
                )
            db_password = db_user.password
            success = db_password == password
            result = LoginType.Success if success else LoginType.IncorrectPassword
            if success:
                user = await User.get_user_from_dbuser(db_user)
                client.user = user
        else:
            result = LoginType.NotRegistered

        await client.send_packet(Login.check_password_result(success, result, user))

    @packet_handler(opcode=InPacket.CLIENT_ERROR)
    async def handle_client_error(self, client, packet: Packet):
        client.close()
        if packet.get_length() < 8:
            debug.error(f"Error: {packet.to_string()}")
            return
        error_str_type = packet.decode_short()
        type_str = ""

        if error_str_type == 0x01:
            type_str = "SendBackupPacket"
        elif error_str_type == 0x02:
            type_str = "CrashReport"
        elif error_str_type == 0x03:
            type_str = "Exception"

        error_type = packet.decode_int()
        data_length = packet.decode_short()
        unk1 = packet.decode_int()

        opcode = packet.decode_short()
        debug.error(f"Error {error_type} at Opcode: {opcode}")

    @packet_handler(opcode=InPacket.WORLD_LIST_REQUEST)
    async def handle_world_list_request(self, client, packet):
        for world in worlds:
            await client.send_packet(
                Login.send_world_information(world, None)
            )
        await client.send_packet(Login.send_world_info_end())
        await client.send_packet(Login.send_recommended_world_msg(WorldId.Scania.value, server_constants.RECOMMEND_MSG))

    @packet_handler(opcode=InPacket.WORLD_STATUS_REQUEST)
    async def handle_world_status_request(self, client, packet):
        world_id = packet.decode_byte()
        await client.send_packet(Login.send_server_status(world_id))

    @packet_handler(opcode=InPacket.SELECT_WORLD)
    async def handle_select_world(self, client: WvsLoginClient, packet):
        unk1 = packet.decode_byte()
        world_id = packet.decode_byte()
        channel = packet.decode_byte() + 1  # We add one cause channels start at index 0 client-side
        success_code = 0
        user = client.user

        account = user.get_account_by_world_id(world_id)
        world = global_states.worlds[0]  # This way only allows us to have one world will change in the furture

        if user is not None and world is not None and world.get_channel_by_id() is not None:
            if account is None:
                account = Account(user=user, world_id=world_id)
                user.add_account(user)
            client.account = account
            client.wid = world_id
            client.channel = channel
