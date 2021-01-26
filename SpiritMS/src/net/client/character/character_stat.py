from src.net.client.character.cards.character_cards import CharacterCards
from src.net.client.character.combat_stat_day_limit import NonCombatStatDayLimit
from src.net.client.character.skill_points import ExtendSP
from src.net.constant.job_constants import *
from src.net.packets.byte_buffer.packet import Packet


class CharacterStat:
    def __init__(
            self,
            chr_stat_id=0,
            chr_id=0,
            chr_id_for_log=0,
            world_id_for_log=0,
            name="",
            gender=0,
            skin=0,
            face=0,
            hair=0,
            mix_base_hair_color=0,
            mix_add_hair_color=0,
            mix_hair_base_prob=0,
            level=0,
            job=0,
            strength=12,
            dex=4,
            inte=4,
            luk=4,
            hp=50,
            max_hp=50,
            mp=5,
            max_mp=5,
            ap=0,
            sp=0,
            exp=0,
            pop=0,  # fame
            money=0,
            wp=0,
            pos_map=100000000,
            portal=0,
            sub_job=0,
            def_face_acc=0,
            fatigue=0,
            last_fatigue_update_time=0,
            charisma_exp=0,
            insight_exp=0,
            will_exp=0,
            craft_exp=0,
            sense_exp=0,
            charm_exp=0,
            pvp_exp=0,
            pvp_grade=0,
            pvp_point=0,
            pvp_mode_level=0,
            pvp_mode_type=0,
            event_point=0,
            alba_activity_id=0,
            alba_start_time=0,
            alba_duration=0,
            alba_special_reward=0,
            burning=False,
            character_card=None,
            extend_sp=None,
            non_combat_stat_day_limit=None,
            gach_exp=0,
            honor_exp=0,
            wing_item=0
    ):
        self._chr_stat_id = chr_stat_id
        self._chr_id = chr_id
        self._chr_id_for_log = chr_id_for_log
        self._world_id_for_log = world_id_for_log
        self._name = name
        self._gender = gender
        self._skin = skin
        self._face = face
        self._hair = hair
        self._mix_base_hair_color = mix_base_hair_color
        self._mix_add_hair_color = mix_add_hair_color
        self._mix_hair_base_prob = mix_hair_base_prob
        self._level = level
        self._job = job
        self._strength = strength
        self._dex = dex
        self._inte = inte
        self._luk = luk
        self._hp = hp
        self._max_hp = max_hp
        self._mp = mp
        self._max_mp = max_mp

        if is_no_mana_job(job):
            self._mp = 0
            self._max_mp = 0

        self._ap = ap
        self._sp = sp
        self._exp = exp
        self._pop = pop  # fame
        self._money = money
        self._wp = wp
        self._pos_map = pos_map
        self._portal = portal
        self._sub_job = sub_job
        self._def_face_acc = def_face_acc
        self._fatigue = fatigue
        self._last_fatigue_update_time = last_fatigue_update_time
        self._charisma_exp = charisma_exp
        self._insight_exp = insight_exp
        self._will_exp = will_exp
        self._craft_exp = craft_exp
        self._sense_exp = sense_exp
        self._charm_exp = charm_exp

        self._pvp_exp = pvp_exp
        self._pvp_grade = pvp_grade
        self._pvp_point = pvp_point
        self._pvp_mode_level = pvp_mode_level
        self._pvp_mode_type = pvp_mode_type
        self._event_point = event_point
        self._alba_activity_id = alba_activity_id
        self._alba_start_time = alba_start_time
        self._alba_duration = alba_duration
        self._alba_special_reward = alba_special_reward
        self._burning = burning

        if character_card is None:
            character_card = CharacterCards()

        self._character_card = character_card

        if extend_sp is None:
            extend_sp = ExtendSP(sub_jobs=7)

        self._extend_sp = extend_sp

        if non_combat_stat_day_limit is None:
            non_combat_stat_day_limit = NonCombatStatDayLimit()

        self._non_combat_stat_day_limit = non_combat_stat_day_limit

        self._gach_exp = gach_exp
        self._honor_exp = honor_exp
        self._wing_item = wing_item

    def encode(self, out_packet: Packet):
        out_packet.encode_int(self.chr_id)
        out_packet.encode_int(self.chr_id_for_log)
        out_packet.encode_int(self.world_id_for_log)
        out_packet.encode_fixed_string(self.name, 13)
        out_packet.encode_byte(self.gender)
        out_packet.encode_byte(self.skin)
        out_packet.encode_int(self.face)
        out_packet.encode_int(self.hair)
        out_packet.encode_byte(self.mix_base_hair_color)
        out_packet.encode_byte(self.mix_add_hair_color)
        out_packet.encode_byte(self.mix_hair_base_prob)
        out_packet.encode_byte(self.level)
        out_packet.encode_short(self.job)
        out_packet.encode_short(self.strength)
        out_packet.encode_short(self.dex)
        out_packet.encode_short(self.inte)
        out_packet.encode_short(self.luk)
        out_packet.encode_int(self.hp)
        out_packet.encode_int(self.max_hp)
        out_packet.encode_int(self.mp)
        out_packet.encode_int(self.max_hp)
        out_packet.encode_short(self.ap)

        if is_extend_sp_job(self.job):
            self.extend_sp.encode(out_packet)
        else:
            out_packet.encode_short(self.sp)

        out_packet.encode_long(self.exp)
        out_packet.encode_int(self.pop)
        out_packet.encode_int(self.wp)
        out_packet.encode_int(self.pos_map)
        out_packet.encode_byte(self.portal)
        out_packet.encode_int(0)  # TODO: Figure out
        out_packet.encode_short(self.sub_job)

        job_id = self.job

        if is_demon(job_id) or is_xenon(job_id) or is_beast_tamer(job_id):
            out_packet.encode_int(self.def_face_acc)

        out_packet.encode_byte(self.fatigue)
        out_packet.encode_int(self.last_fatigue_update_time)
        out_packet.encode_int(self.charisma_exp)
        out_packet.encode_int(self.insight_exp)
        out_packet.encode_int(self.will_exp)
        out_packet.encode_int(self.craft_exp)
        out_packet.encode_int(self.sense_exp)
        out_packet.encode_int(self.charm_exp)

        self.non_combat_stat_day_limit.encode(out_packet)

        out_packet.encode_int(self.pvp_exp)
        out_packet.encode_byte(self.pvp_grade)
        out_packet.encode_int(self.pvp_point)
        out_packet.encode_byte(2)

        out_packet.encode_byte(self.pvp_mode_type)
        out_packet.encode_int(self.event_point)
        out_packet.encode_byte(self.alba_activity_id)
        out_packet.encode_ft(None)  # self.alba_start_time
        out_packet.encode_int(self.alba_duration)
        out_packet.encode_byte(self.alba_special_reward)

        # TODO: characterCard
        self.character_card.encode(out_packet)

        out_packet.encode_ft(None)  # self.last_logout
        out_packet.encode_byte(self.burning)

    @property
    def chr_stat_id(self):
        return self._chr_stat_id

    @chr_stat_id.setter
    def chr_stat_id(self, x):
        self._chr_stat_id = x

    @property
    def chr_id(self):
        return self._chr_id

    @chr_id.setter
    def chr_id(self, new_chr_id):
        self._chr_id = new_chr_id

    @property
    def chr_id_for_log(self):
        return self._chr_id_for_log

    @chr_id_for_log.setter
    def chr_id_for_log(self, chr_id_for_log):
        self._chr_id_for_log = chr_id_for_log

    @property
    def world_id_for_log(self):
        return self._world_id_for_log

    @world_id_for_log.setter
    def world_id_for_log(self, wid_for_log):
        self._world_id_for_log = wid_for_log

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

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
    def mix_base_hair_color(self):
        return self._mix_base_hair_color

    @mix_base_hair_color.setter
    def mix_base_hair_color(self, mbhc):
        self._mix_base_hair_color = mbhc

    @property
    def mix_add_hair_color(self):
        return self._mix_add_hair_color

    @mix_add_hair_color.setter
    def mix_add_hair_color(self, mahc):
        self._mix_add_hair_color = mahc

    @property
    def mix_hair_base_prob(self):
        return self._mix_hair_base_prob

    @mix_hair_base_prob.setter
    def mix_hair_base_prob(self, mhbp):
        self._mix_hair_base_prob = mhbp

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, new_level):
        self._level = new_level

    @property
    def job(self):
        return self._job

    @job.setter
    def job(self, job_id):
        self._job = job_id

    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, new_str):
        self._strength = new_str

    @property
    def dex(self):
        return self._dex

    @dex.setter
    def dex(self, new_dex):
        self._dex = new_dex

    @property
    def inte(self):
        return self._inte

    @property
    def luk(self):
        return self._luk

    @luk.setter
    def luk(self, new_luk):
        self._luk = new_luk

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, new_hp):
        self._hp = new_hp

    @property
    def max_hp(self):
        return self._max_hp

    @max_hp.setter
    def max_hp(self, new_max_hp):
        self._max_hp = new_max_hp

    @property
    def mp(self):
        return self._mp

    @mp.setter
    def mp(self, new_mp):
        self._mp = new_mp

    @property
    def max_mp(self):
        return self._max_mp

    @max_mp.setter
    def max_mp(self, new_max_mp):
        self._max_mp = new_max_mp

    @property
    def ap(self):
        return self._ap

    @ap.setter
    def ap(self, new_ap):
        self._ap = new_ap  # AP = Ability Power

    @property
    def sp(self):
        return self._sp  # SP = Skill Points

    @sp.setter
    def sp(self, new_sp):
        self._sp = new_sp

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, new_exp):
        self._exp = new_exp

    @property
    def pop(self):
        return self._pop

    @pop.setter
    def pop(self, new_pop):
        self._pop = new_pop

    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, new_money):
        self._money = new_money

    @property
    def wp(self):
        return self._wp

    @wp.setter
    def wp(self, new_wp):
        self._wp = new_wp

    @property
    def pos_map(self):
        return self._pos_map

    @pos_map.setter
    def pos_map(self, new_map):
        self._pos_map = new_map

    @property
    def portal(self):
        return self._portal

    @portal.setter
    def portal(self, portal_id):
        self._portal = portal_id

    @property
    def sub_job(self):
        return self._sub_job

    @sub_job.setter
    def sub_job(self, sub_job_id):
        self._sub_job = sub_job_id

    @property
    def def_face_acc(self):
        return self._def_face_acc

    @def_face_acc.setter
    def def_face_acc(self, def_face_acc_id):
        self._def_face_acc = def_face_acc_id

    @property
    def fatigue(self):
        return self._fatigue

    @fatigue.setter
    def fatigue(self, fatigue_time):
        self._fatigue = fatigue_time

    @property
    def last_fatigue_update_time(self):
        return self._last_fatigue_update_time

    @last_fatigue_update_time.setter
    def last_fatigue_update_time(self, lfut):
        self._last_fatigue_update_time = lfut

    @property
    def charisma_exp(self):
        return self._charisma_exp

    @charisma_exp.setter
    def charisma_exp(self, new_charisma_exp):
        self._charisma_exp = new_charisma_exp

    @property
    def insight_exp(self):
        return self._insight_exp

    @insight_exp.setter
    def insight_exp(self, new_insight_exp):
        self._insight_exp = new_insight_exp

    @property
    def will_exp(self):
        return self._will_exp

    @will_exp.setter
    def will_exp(self, new_will_exp):
        self._will_exp = new_will_exp

    @property
    def craft_exp(self):
        return self._craft_exp

    @craft_exp.setter
    def craft_exp(self, new_craft_exp):
        self._craft_exp = new_craft_exp

    @property
    def sense_exp(self):
        return self._sense_exp

    @sense_exp.setter
    def sense_exp(self, new_sense_exp):
        self._sense_exp = new_sense_exp

    @property
    def charm_exp(self):
        return self._charm_exp

    @charm_exp.setter
    def charm_exp(self, new_charm_exp):
        self._charm_exp = new_charm_exp

    @property
    def pvp_exp(self):
        return self._pvp_exp

    @pvp_exp.setter
    def pvp_exp(self, new_pvp_exp):
        self._pvp_exp = new_pvp_exp

    @property
    def pvp_grade(self):
        return self._pvp_grade

    @pvp_grade.setter
    def pvp_grade(self, new_pvp_grade):
        self._pvp_grade = new_pvp_grade

    @property
    def pvp_point(self):
        return self._pvp_point

    @pvp_point.setter
    def pvp_point(self, new_pvp_point):
        self._pvp_point = new_pvp_point

    @property
    def pvp_mode_level(self):
        return self._pvp_mode_level

    @pvp_mode_level.setter
    def pvp_mode_level(self, new_pvp_mode_level):
        self._pvp_mode_level = new_pvp_mode_level

    @property
    def pvp_mode_type(self):
        return self._pvp_mode_type

    @pvp_mode_type.setter
    def pvp_mode_type(self, new_pvp_mode_type):
        self._pvp_mode_type = new_pvp_mode_type

    @property
    def event_point(self):
        return self._event_point

    @event_point.setter
    def event_point(self, new_event_point):
        self._event_point = new_event_point

    @property
    def alba_activity_id(self):
        return self._alba_activity_id

    @alba_activity_id.setter
    def alba_activity_id(self, new_alba_activity_id):
        self._alba_activity_id = new_alba_activity_id

    @property
    def alba_start_time(self):
        return self._alba_start_time

    @alba_start_time.setter
    def alba_start_time(self, new_alba_start_time):
        self._alba_start_time = new_alba_start_time

    @property
    def alba_duration(self):
        return self._alba_duration

    @alba_duration.setter
    def alba_duration(self, new_alba_duration):
        self._alba_duration = new_alba_duration

    @property
    def alba_special_reward(self):
        return self._alba_special_reward

    @alba_special_reward.setter
    def alba_special_reward(self, new_alba_special_reward):
        self._alba_special_reward = new_alba_special_reward

    @property
    def burning(self):
        return self._burning

    @burning.setter
    def burning(self, new_burning: bool):
        self._burning = new_burning

    @property
    def character_card(self):
        return self._character_card

    @character_card.setter
    def character_card(self, new_character_card: bool):
        self._character_card = new_character_card

    @property
    def extend_sp(self):
        return self._extend_sp

    @extend_sp.setter
    def extend_sp(self, extend_sp):
        self._extend_sp = extend_sp

    @property
    def non_combat_stat_day_limit(self):
        return self._non_combat_stat_day_limit

    @non_combat_stat_day_limit.setter
    def non_combat_stat_day_limit(self, non_csdl):
        self._non_combat_stat_day_limit = non_csdl

    @property
    def gach_exp(self):
        return self._gach_exp

    @gach_exp.setter
    def gach_exp(self, new_gach_exp: bool):
        self._gach_exp = new_gach_exp

    @property
    def honor_exp(self):
        return self._honor_exp

    @honor_exp.setter
    def honor_exp(self, new_honor_exp: bool):
        self._honor_exp = new_honor_exp

    @property
    def wing_item(self):
        return self._wing_item

    @wing_item.setter
    def wing_item(self, new_wing_item: bool):
        self._wing_item = new_wing_item
