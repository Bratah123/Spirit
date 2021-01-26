from src.net.packets.byte_buffer.packet import Packet


class NonCombatStatDayLimit:
    def __init__(
            self,
            combat_id=0,
            charisma=0,
            charm=0,
            insight=0,
            will=0,
            craft=0,
            sense=0,
            last_update_charm_by_cash_pr=None,
            charm_by_cash_pr=0,
    ):
        self._combat_id = combat_id
        self._charisma = charisma
        self._charm = charm
        self._insight = insight
        self._will = will
        self._craft = craft
        self._sense = sense
        self._last_update_charm_by_cash_pr = last_update_charm_by_cash_pr
        self._charm_by_cash_pr = charm_by_cash_pr

    def encode(self, out_packet: Packet):
        out_packet.encode_short(self._charisma)
        out_packet.encode_short(self._insight)
        out_packet.encode_short(self._will)
        out_packet.encode_short(self._craft)
        out_packet.encode_short(self._sense)
        out_packet.encode_short(self._charm)
        out_packet.encode_byte(self._charm_by_cash_pr)
        out_packet.encode_ft(self._last_update_charm_by_cash_pr)