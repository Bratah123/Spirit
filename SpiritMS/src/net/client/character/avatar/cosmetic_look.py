from src.net.constant import job_constants, item_constants
from src.net.packets.byte_buffer.packet import Packet


class CosmeticLook:
    def __init__(
            self,
            cosmetic_look_id=0,
            gender=0,
            skin=0,
            face=0,
            hair=0,
            weapon_sticker_id=0,
            weapon_id=0,
            sub_weapon_id=0,
            hair_equips=None,
            unseen_equips=None,
            pet_ids=None,
            job_id=0,
            draw_elf_ears=False,
            demon_slayer_def_face_acc=0,
            xenon_def_face_acc=0,
            beast_tamer_def_face_acc=0,
            is_zero_beta_look=False,
            mixed_hair_color=0,
            mix_hair_percent=0,
            ears=0,
            tail=0,
            demon_wing_id=0,
            kaiser_wing_id=0,
            kaiser_tail_id=0,
    ):
        self._id = cosmetic_look_id
        self._gender = gender
        self._skin = skin
        self._face = face
        self._hair = hair
        self._weapon_sticker_id = weapon_sticker_id
        self._weapon_id = weapon_id
        self._sub_weapon_id = sub_weapon_id

        if unseen_equips is None:
            unseen_equips = []
        if hair_equips is None:
            hair_equips = []
        if pet_ids is None:
            pet_ids = [0, 0, 0]

        self._hair_equips = hair_equips
        self._unseen_equips = unseen_equips
        self._pet_ids = pet_ids

        self._job_id = job_id
        self._draw_elf_ears = draw_elf_ears

        self._demon_slayer_def_face_acc = demon_slayer_def_face_acc
        self._xenon_def_face_acc = xenon_def_face_acc
        self._beast_tamer_def_face_acc = beast_tamer_def_face_acc
        self._is_zero_beta_look = is_zero_beta_look
        self._mixed_hair_color = mixed_hair_color
        self._mix_hair_percent = mix_hair_percent

        self._totems = []

        self._ears = ears
        self._tail = tail

        self._demon_wing_id = demon_wing_id
        self._kaiser_wing_id = kaiser_wing_id
        self._kaiser_tail_id = kaiser_tail_id

    def encode(self, out_packet: Packet):
        out_packet.encode_byte(self.gender)
        out_packet.encode_byte(self.skin)
        out_packet.encode_int(self.face)
        out_packet.encode_int(self.job_id)
        out_packet.encode_byte(0)  # ignored
        out_packet.encode_int(self.hair)

        for item_id in self.hair_equips:
            body_part = item_constants.get_body_part_from_item(item_id, self.gender)
            if body_part != 0:
                out_packet.encode_byte(body_part)
                out_packet.encode_int(item_id)

        out_packet.encode_byte(-1)  # idk what it does
        for item_id in self.unseen_equips:
            body_part = item_constants.get_body_part_from_item(item_id, self.gender)
            out_packet.encode_byte(body_part)
            out_packet.encode_int(item_id)

        out_packet.encode_byte(-1)  # idk what it does
        for item_id in self.totems:
            body_part = item_constants.get_body_part_from_item(item_id, self.gender)
            out_packet.encode_byte(body_part)
            out_packet.encode_int(item_id)

        out_packet.encode_byte(-1)  # idk bruh

        out_packet.encode_int(self.weapon_sticker_id)
        out_packet.encode_int(self.weapon_id)
        out_packet.encode_int(self.sub_weapon_id)
        out_packet.encode_int(self.draw_elf_ears)

        pet_amount = len(self.pet_ids)
        for i in range(3):
            if pet_amount > i:
                out_packet.encode_int(self.pet_ids[i])
            else:
                out_packet.encode_int(0)

        if job_constants.is_zero(self.job_id):
            out_packet.encode_byte(self.is_zero_beta_look)
        if job_constants.is_xenon(self.job_id):
            out_packet.encode_int(self.xenon_def_face_acc)
        if job_constants.is_beast_tamer(self.job_id):
            out_packet.encode_int(self.demon_slayer_def_face_acc)
        if job_constants.is_beast_tamer(self.job_id):
            has_ears = self.ears > 0
            has_tail = self.tail > 0
            out_packet.encode_int(self.beast_tamer_def_face_acc)
            out_packet.encode_byte(has_ears)
            out_packet.encode_int(self.ears)
            out_packet.encode_byte(has_tail)
            out_packet.encode_int(self.tail)

        out_packet.encode_byte(self.mixed_hair_color)
        out_packet.encode_byte(self.mix_hair_percent)

    @property
    def cosmetic_look_id(self):
        return self._id

    @cosmetic_look_id.setter
    def cosmetic_look_id(self, cos_id):
        self._id = cos_id

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender_id):
        self._gender = gender_id

    @property
    def skin(self):
        return self._skin

    @skin.setter
    def skin(self, skin_id):
        self._skin = skin_id

    @property
    def face(self):
        return self._face

    @face.setter
    def face(self, face_id):
        self._face = face_id

    @property
    def hair(self):
        return self._hair

    @hair.setter
    def hair(self, hair_id):
        self._hair = hair_id

    @property
    def weapon_sticker_id(self):
        return self._weapon_sticker_id

    @weapon_sticker_id.setter
    def weapon_sticker_id(self, wep_sticker_id):
        self._weapon_sticker_id = wep_sticker_id

    @property
    def weapon_id(self):
        return self._weapon_id

    @weapon_id.setter
    def weapon_id(self, wep_id):
        self._weapon_id = wep_id

    @property
    def sub_weapon_id(self):
        return self._sub_weapon_id

    @sub_weapon_id.setter
    def sub_weapon_id(self, sub_wep_id):
        self._sub_weapon_id = sub_wep_id

    @property
    def hair_equips(self):
        return self._hair_equips

    @hair_equips.setter
    def hair_equips(self, hair_equips):
        self._hair_equips = list(hair_equips)

    @property
    def unseen_equips(self):
        return self._unseen_equips

    @unseen_equips.setter
    def unseen_equips(self, unseen_equips):
        self._unseen_equips = list(unseen_equips)

    @property
    def pet_ids(self):
        return self._pet_ids

    @pet_ids.setter
    def pet_ids(self, pet_ids):
        self._pet_ids = list(pet_ids)

    @property
    def job_id(self):
        return self._job_id

    @job_id.setter
    def job_id(self, new_job_id):
        self._job_id = new_job_id

    @property
    def draw_elf_ears(self):
        return self._draw_elf_ears

    @draw_elf_ears.setter
    def draw_elf_ears(self, draw: bool):
        self._draw_elf_ears = draw

    @property
    def demon_slayer_def_face_acc(self):
        return self._demon_slayer_def_face_acc

    @demon_slayer_def_face_acc.setter
    def demon_slayer_def_face_acc(self, ds_def_face_acc):
        self._demon_slayer_def_face_acc = ds_def_face_acc

    @property
    def xenon_def_face_acc(self):
        return self._xenon_def_face_acc

    @xenon_def_face_acc.setter
    def xenon_def_face_acc(self, xenon_face_acc):
        self._xenon_def_face_acc = xenon_face_acc

    @property
    def beast_tamer_def_face_acc(self):
        return self._beast_tamer_def_face_acc

    @beast_tamer_def_face_acc.setter
    def beast_tamer_def_face_acc(self, bt_def_face_acc):
        self._beast_tamer_def_face_acc = bt_def_face_acc

    @property
    def is_zero_beta_look(self):
        return self._is_zero_beta_look

    @is_zero_beta_look.setter
    def is_zero_beta_look(self, zero_look: bool):
        self._is_zero_beta_look = zero_look

    @property
    def mixed_hair_color(self):
        return self._mixed_hair_color

    @mixed_hair_color.setter
    def mixed_hair_color(self, mixed_hair_id):
        self._mixed_hair_color = mixed_hair_id

    @property
    def mix_hair_percent(self):
        return self._mix_hair_percent

    @mix_hair_percent.setter
    def mix_hair_percent(self, percent):
        self._mix_hair_percent = percent

    @property
    def totems(self):
        return self._totems

    @totems.setter
    def totems(self, totems):
        self._totems = list(totems)

    @property
    def ears(self):
        return self._ears

    @ears.setter
    def ears(self, ear_id):
        self._ears = ear_id

    @property
    def tail(self):
        return self._tail

    @tail.setter
    def tail(self, tail_id):
        self._tail = tail_id

    @property
    def demon_wing_id(self):
        return self._demon_wing_id

    @demon_wing_id.setter
    def demon_wing_id(self, d_wing_id):
        self._demon_wing_id = d_wing_id

    @property
    def kaiser_wing_id(self):
        return self._kaiser_wing_id

    @kaiser_wing_id.setter
    def kaiser_wing_id(self, k_wing_id):
        self._kaiser_wing_id = k_wing_id

    @property
    def kaiser_tail_id(self):
        return self._kaiser_tail_id

    @kaiser_tail_id.setter
    def kaiser_tail_id(self, k_tail_id):
        self._kaiser_tail_id = k_tail_id
