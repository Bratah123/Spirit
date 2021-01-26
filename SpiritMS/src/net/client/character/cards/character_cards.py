from src.net.packets.byte_buffer.packet import Packet


class CharacterCards:
    def __init__(
            self,
            card_id=0,
            char_id=0,
            job=0,
            level=0,
    ):
        self._card_id = card_id
        self._char_id = char_id
        self._job = job
        self._level = level

    @property
    def card_id(self):
        return self._card_id

    @card_id.setter
    def card_id(self, new_id):
        self._card_id = new_id

    @property
    def char_id(self):
        return self._char_id

    @char_id.setter
    def char_id(self, new_id):
        self._char_id = new_id

    @property
    def job(self):
        return self._job

    @job.setter
    def job(self, new_id):
        self._job = new_id

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, new_level):
        self._level = new_level

    def encode(self, out_packet: Packet):
        for i in range(9):
            out_packet.encode_int(self.char_id)
            out_packet.encode_int(self.level)
            out_packet.encode_int(self.job)
