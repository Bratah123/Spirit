"""
Static "class"
@author Brandon
Created: 8/21/2020
"""
from typing import Tuple, List

from src.net.client.account import Account
from src.net.client.user import User
from src.net.constant import job_constants
from src.net.enum.login_type import LoginType
from src.net.enum.server_status import ServerStatus
from src.net.packets.send_ops import OutPacket
from src.net.packets.byte_buffer.packet import Packet
from src.net.server import server_constants
from src.net.server.global_states import worlds
from src.net.server.server_constants import CHAT_PORT
from src.net.world.world import World


class Login:

    @staticmethod
    def send_connect(siv, riv):

        send_packet = Packet(opcode=15)

        send_packet.encode_short(server_constants.SERVER_VERSION)
        send_packet.encode_string(server_constants.MINOR_VERSION)
        send_packet.encode_int(riv)
        send_packet.encode_int(siv)
        send_packet.encode_byte(server_constants.LOCALE)

        return send_packet

    @staticmethod
    def send_auth_server(use_auth_server: bool):
        """
        :param use_auth_server: boolean
        :return: Packet
        """
        send_packet = Packet(opcode=OutPacket.AUTH_SERVER)

        send_packet.encode_byte(use_auth_server)

        return send_packet

    @staticmethod
    def send_start_client():
        """Returns the client start packet

        :return: Packet
        """
        send_packet = Packet(opcode=OutPacket.CLIENT_START)

        send_packet.encode_byte(False)  # encode byte

        return send_packet

    @staticmethod
    def send_auth_response(response: bool):
        send_packet = Packet(opcode=OutPacket.PRIVATE_SERVER_PACKET)

        send_packet.encode_int(response)

        return send_packet

    @staticmethod
    def check_password_result(success: bool, login_type: LoginType, user: User) -> Packet:

        send_packet = Packet(opcode=OutPacket.CHECK_PASSWORD_RESULT)

        if success:
            send_packet.encode_byte(LoginType.Success.value)
            send_packet.encode_byte(0)
            send_packet.encode_int(0)
            send_packet.encode_string(user.name)
            send_packet.encode_int(user.user_id)
            send_packet.encode_byte(user.gender)
            send_packet.encode_byte(user.msg2)
            send_packet.encode_int(user.acc_type.value)
            send_packet.encode_int(user.age)

            has_censored = user.has_censored_nx_login_id

            send_packet.encode_byte(not has_censored)
            if has_censored:
                send_packet.encode_string(user.censored_nx_login_id)

            send_packet.encode_string(user.name)
            send_packet.encode_byte(user.p_block_reason)
            send_packet.encode_byte(0)  # unknown
            send_packet.encode_long(user.chat_unblock_date)
            send_packet.encode_long(user.chat_unblock_date)
            send_packet.encode_int(user.character_slots + 3)
            job_constants.encode(send_packet)
            send_packet.encode_byte(user.grade_code)
            send_packet.encode_int(0)  # Enable Star Planet
            send_packet.encode_byte(0)  # Unknown
            send_packet.encode_byte(0)  # Unknown
            send_packet.encode_ft(user.creation_date)
        elif login_type == LoginType.Blocked:
            send_packet.encode_byte(login_type.value)
            send_packet.encode_byte(0)
            send_packet.encode_int(0)
            send_packet.encode_byte(0)
            send_packet.encode_ft(None)  # FileTime is not handled atm
        else:
            send_packet.encode_byte(login_type.value)
            send_packet.encode_byte(0)
            send_packet.encode_int(0)

        return send_packet

    @staticmethod
    def send_world_information(world: World, string_infos: List[Tuple]):
        send_packet = Packet(opcode=OutPacket.WORLD_INFORMATION)

        send_packet.encode_byte(world.world_id)
        send_packet.encode_string(world.name)
        send_packet.encode_byte(world.world_state)
        send_packet.encode_string(world.world_event_description)
        send_packet.encode_short(world.world_event_exp_wse)
        send_packet.encode_short(world.world_event_drop_wse)
        send_packet.encode_byte(world.char_create_block)
        send_packet.encode_byte(world.get_channel_size())

        for channel in world.channels:
            send_packet.encode_string(channel.name)
            send_packet.encode_int(channel.get_gauge_percent())
            send_packet.encode_byte(channel.world_id)
            send_packet.encode_byte(channel.channel_id)
            send_packet.encode_byte(channel.adult_channel)

        if string_infos is None:
            send_packet.encode_short(0)
        else:
            send_packet.encode_short(len(string_infos))
            for string_info in string_infos:
                send_packet.encode_position(string_info[0])
                send_packet.encode_string(string_info[1])

        send_packet.encode_int(0)  # some Offset
        send_packet.encode_byte(world.star_planet)

        return send_packet

    @staticmethod
    def send_world_info_end():
        send_packet = Packet(opcode=OutPacket.WORLD_INFORMATION)
        send_packet.encode_int(255)
        return send_packet

    @staticmethod
    def send_recommended_world_msg(world_id, msg):
        send_packet = Packet(opcode=OutPacket.RECOMMENDED_WORLD_MESSAGE)
        send_packet.encode_byte(1)
        send_packet.encode_int(world_id)
        send_packet.encode_string(msg)
        return send_packet

    @staticmethod
    def send_server_status(world_id):
        send_packet = Packet(opcode=OutPacket.SERVER_STATUS)
        world = None
        for world_created in worlds:
            if world_created.world_id == world_id:
                world = world_created
        if world is not None and not world.is_full():
            send_packet.encode_byte(ServerStatus.NORMAL.value)
        else:
            send_packet.encode_byte(ServerStatus.BUSY.value)

        send_packet.encode_byte(0)  # unknown

        return send_packet

    @staticmethod
    def select_world_result(user: User, account: Account, success_code, special_server, burning_event_block):
        send_packet = Packet(opcode=OutPacket.SELECT_WORLD_RESULT)
        send_packet.encode_byte(success_code)
        send_packet.encode_string(special_server)
        send_packet.encode_int(20)  # trunk/storage slot count
        send_packet.encode_byte(burning_event_block)

        reserved = 0
        send_packet.encode_int(reserved)  # Reserved size

        send_packet.encode_ft(None)
        for i in range(reserved):
            # FileTime
            send_packet.encode_int(0)
            # ft.encode()

        is_edited = False
        send_packet.encode_byte(is_edited)

        chars = account.characters
        chars.sort()
        char_size = len(chars)

        for char in chars:
            send_packet.encode_int(char.id)

        send_packet.encode_byte(char_size)

        for char in chars:
            pass

        send_packet.encode_byte(user.get_pic_status())
        send_packet.encode_byte(False)  # bQuerySSNOnCreateNewCharacter
        send_packet.encode_int(user.character_slots)
        send_packet.encode_int(0)
        send_packet.encode_int(0)  # nEventNewCharJob
        send_packet.encode_ft(None)
        send_packet.encode_byte(0)  # RenameCount
        send_packet.encode_byte(0)

        return send_packet

    @staticmethod
    def select_character_result(login_type: LoginType, error_code, port, character_id):
        send_packet = Packet(opcode=OutPacket.SELECT_CHARACTER_RESULT)
        send_packet.encode_byte(login_type.value)
        send_packet.encode_byte(error_code)
        if login_type == LoginType.Success:
            server = [8, 31, 99, 141]
            send_packet.encode_arr(server)
            send_packet.encode_short(port)

            chat_server = [8, 31, 99, 141]
            send_packet.encode_arr(chat_server)
            send_packet.encode_short(CHAT_PORT)

            send_packet.encode_int(character_id)
            send_packet.encode_byte(0)
            send_packet.encode_int(0) # ulArgument
            send_packet.encode_byte(0)
            send_packet.encode_int(0)
            send_packet.encode_int(0)
            send_packet.encode_byte(0)

        return send_packet
