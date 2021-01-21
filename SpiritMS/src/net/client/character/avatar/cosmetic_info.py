from src.net.constant import job_constants


class CosmeticInfo:
    def __init__(self, cosmetic_id=0, cosmetic_look=None, character_stat=None, zero_cosmetic_look=None):
        self._id = cosmetic_id
        self._cosmetic_look = cosmetic_look
        self._zero_cosmetic_look = zero_cosmetic_look
        self._character_stat = character_stat

    @property
    def cosmetic_look(self):
        return self._cosmetic_look

    def get_cosmetic_look(self, zero_beta_state: bool):
        return self.zero_cosmetic_look if zero_beta_state else self.cosmetic_look

    @property
    def character_stat(self):
        return self._character_stat

    @character_stat.setter
    def character_stat(self, char_stat):
        self._character_stat = char_stat

    @property
    def cosmetic_id(self):
        return self._id

    @cosmetic_id.setter
    def cosmetic_id(self, cos_id):
        self._id = cos_id

    @property
    def zero_cosmetic_look(self):
        return self._zero_cosmetic_look

    @zero_cosmetic_look.setter
    def zero_cosmetic_look(self, zero_cos_look):
        self._zero_cosmetic_look = zero_cos_look

    @cosmetic_look.setter
    def cosmetic_look(self, value):
        self._cosmetic_look = value

    def encode_cosmetic(self, out_packet):
        self.character_stat.encode(out_packet)
        self.cosmetic_look.encode(out_packet)
        if job_constants.is_zero(self.character_stat.job):
            self.zero_cosmetic_look.encode()


