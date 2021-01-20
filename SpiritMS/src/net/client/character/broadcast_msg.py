from src.net.enum.broadcast_msg_type import BroadcastMsgType


class BroadcastMsg:

    def __init__(self, string1="", broadcast_type=None):
        self.broadcast_msg_type = broadcast_type
        self.item = None
        self.string1 = string1
        self.string2 = ""
        self.string3 = ""
        self.arg1 = 0
        self.arg2 = 0
        self.arg3 = 0

    def encode(self, out_packet):
        out_packet.encode_byte(self.broadcast_msg_type.value)
        out_packet.encode_string(self.string1)
        broadcast_type = self.broadcast_msg_type

        if broadcast_type == BroadcastMsgType.Megaphone or broadcast_type == BroadcastMsgType.MegaphoneNoMessage:
            out_packet.encode_byte(self.arg1)
            out_packet.encode_byte(self.arg2)

    @staticmethod
    def pop_up_message(message):
        bMsg = BroadcastMsg(
            string1=message,
            broadcast_type=BroadcastMsgType.PopUpMessage
        )
        return bMsg

