from src.net.packets.byte_buffer.packet import Packet


class Advertisement:
    """
    Class that represents the advertisement on world selection
    Change default values in the __init__ method
    """
    def __init__(
            self,
            striking_image="",
            address_to_move="",
            duration=5000,
            width=310,
            height=60,
            x_pos=235,
            y_pos=538,
    ):
        self.striking_image = striking_image
        self.address_to_move = address_to_move
        self.duration = duration
        self.width = width
        self.height = height
        self.x_pos = x_pos
        self.y_pos = y_pos

    def encode(self, out_packet: Packet):
        out_packet.encode_string(self.striking_image)
        out_packet.encode_string(self.address_to_move)
        out_packet.encode_int(self.duration)
        out_packet.encode_int(self.width)
        out_packet.encode_int(self.height)
        out_packet.encode_int(self.x_pos)
        out_packet.encode_int(self.y_pos)