from src.net.client.account import Account
from src.net.client.character.broadcast_msg import BroadcastMsg
from src.net.client.character.character import Character
from src.net.client.packet_client import WvsLoginClient
from src.net.client.user import User
from src.net.connections.database import database_manager
from src.net.connections.packet.wvs_context import WvsContext
from src.net.constant import job_constants
from src.net.constant.game_constants import BLOCKED_NAMES
from src.net.debug import debug
from src.net.enum.char_name_result import CharNameResult
from src.net.enum.login_type import LoginType
from src.net.enum.world_id import WorldId
from src.net.handlers.packet_handler import packet_handler
from src.net.login.login import Login
from src.net.packets.byte_buffer.packet import Packet
from src.net.packets.recv_ops import InPacket
from src.net.packets.send_ops import OutPacket
from src.net.server import server_constants, global_states
from src.net.server.global_states import worlds
from src.net.server.server_constants import AUTO_REGISTER


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
        """Where logging in is handled, passwords/username etc"""
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

        if db_user is None and AUTO_REGISTER:
            # if there is no user in the database we register one
            await database_manager.register_user(username, password)
            await client.send_packet(
                WvsContext.broadcast_msg(
                    BroadcastMsg.pop_up_message("Your account has now been registered.")
                )
            )

        if db_user is not None:
            if password.lower() == "fixme":
                # TODO, implement a loggedin check
                await client.send_packet(
                    WvsContext.broadcast_msg(BroadcastMsg.pop_up_message("Your account is now logged out."))
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

        if len(user.accounts) > 0:
            account = user.accounts[0]
            # We get the first one cause user should only have one account in this source
        else:
            account = user.get_account_from_db()

        world = global_states.worlds[0]  # This way only allows us to have one world will change in the future

        if user is not None and world is not None and world.get_channel_by_id(channel) is not None:
            if account is None:
                account = Account(user=user, world_id=world_id)
                await database_manager.create_account(account)  # create a new row in SQL if account doesn't exist
            user.add_account(account)
            client.account = account
            client.wid = world_id
            client.channel = channel

            await client.send_packet(
                Login.select_world_result(
                    user=client.user,
                    account=client.account,
                    success_code=success_code,
                    special_server="normal",
                    burning_event_block=False
                )
            )
        else:
            await client.send_packet(
                Login.select_character_result(
                    login_type=LoginType.UnauthorizedUser,
                    error_code=0,
                    port=0,
                    character_id=0,
                )
            )

    @packet_handler(opcode=InPacket.WORLD_INFO_REQUEST)
    async def handle_world_info_request(self, client: WvsLoginClient, packet: Packet):
        for world in global_states.worlds:
            await client.send_packet(Login.send_world_information(world, None))
        await client.send_packet(Login.send_world_info_end())

    @packet_handler(opcode=InPacket.CHECK_DUPLICATE_ID)
    async def handle_check_duplicate_id(self, client: WvsLoginClient, packet: Packet):
        name = packet.decode_string()
        code = None
        if name.lower() in BLOCKED_NAMES:
            code = CharNameResult.Unavailable_Invalid
        else:
            name_taken = await database_manager.check_name_taken(name)
            code = CharNameResult.Unavailable_InUse if name_taken else CharNameResult.Available

        await client.send_packet(Login.check_duplicated_id_result(name, code))

    @packet_handler(opcode=InPacket.CREATE_NEW_CHARACTER)
    async def handle_create_new_char(self, client: WvsLoginClient, packet: Packet):
        account = client.account
        name = packet.decode_string()
        key_setting_type = packet.decode_int()
        event_new_char_sale_job = packet.decode_int()
        cur_selected_race = packet.decode_int()
        job = job_constants.get_login_job_by_id(cur_selected_race)[2]
        cur_selected_sub_job = packet.decode_short()
        gender = packet.decode_byte()
        skin = packet.decode_byte()

        item_length = packet.decode_byte()
        items = [packet.decode_int() for i in range(item_length)]

        face = items[0]
        hair = items[1]

        name_result_code = None
        # Add a check if starting items are valid
        if skin > 13:
            name_result_code = CharNameResult.Unavailable_CashItem

        name_taken = await database_manager.check_name_taken(name)

        if name in BLOCKED_NAMES:
            name_result_code = CharNameResult.Unavailable_Invalid
        elif name_taken:
            name_result_code = CharNameResult.Unavailable_InUse

        if name_result_code is not None:
            await client.send_packet(Login.check_duplicated_id_result(name, name_result_code))
            return
        char_id = await database_manager.get_next_available_chr_id()
        char = Character(
            chr_id=char_id,
            acc_id=account.account_id,
            key_setting_type=key_setting_type,
            name=name,
            job_id=job.value[0],
            cur_selected_sub_job=cur_selected_sub_job,
            gender=gender,
            skin=skin,
            face=face,
            hair=hair,
            items=items,
        )

        # TODO: Add Job Manager to Char
        await char.init_in_db()
        char_stat = char.cosmetic_info.character_stat

        if cur_selected_race == job_constants.LOGIN_JOB['DUAL_BLADE'][0]:
            char_stat.sub_job = 1

        char_stat.chr_id = char.chr_id
        char_stat.chr_id_for_log = char.chr_id
        char_stat.world_id_for_log = account.world_id

        for hair_id in char.cosmetic_info.cosmetic_look.hair_equips:
            # TODO: Add item to inventory
            pass

        # TODO: Codex
        account.characters.append(char)
        await account.save()
        await client.send_packet(
            Login.create_new_char_result(LoginType.Success, char)
        )
