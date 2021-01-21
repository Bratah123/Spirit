class CosmeticLook:
    def __init__(
            self,
            cosmetic_look_id,
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
        self._hair_equips = hair_equips

    @property
    def unseen_equips(self):
        return self._unseen_equips

    @unseen_equips.setter
    def unseen_equips(self, unseen_equips):
        self._unseen_equips = unseen_equips

    @property
    def pet_ids(self):
        return self._pet_ids

    @pet_ids.setter
    def pet_ids(self, pet_ids):
        self._pet_ids = pet_ids

    @property
    def job_id(self):
        return self._job_id

    @job_id.setter
    def job_id(self, new_job_id):
        self._job_id = new_job_id

    