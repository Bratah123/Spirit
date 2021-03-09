from src.net.debug import debug
from src.net.enum import equip_prefix
from src.net.enum.body_part import BodyPart
from src.net.enum.equip_prefix import EquipPrefix


# Side note for future developers: // operator is floor division meaning it removes decimals

def is_equip(item_id):
    return item_id // 1000000 == 1


def get_item_prefix(item_id):
    return item_id // 10000


def get_gender_from_id(item_id):
    if item_id // 1000000 != 1 and get_item_prefix(item_id) or get_item_prefix(item_id) == 119 or get_item_prefix(
            item_id) == 168:
        return 2
    check = (item_id // 1000) % 10

    if check == 0:
        return 0
    elif check == 1:
        return 1
    else:
        return 2


def is_long_or_big_sword(item_id):
    item_prefix = get_item_prefix(item_id)
    return item_prefix == EquipPrefix.Lapis.value or item_prefix == EquipPrefix.Lazuli.value


def is_weapon(item_id):
    return 1210000 <= item_id < 1600000


def is_fan(item_id):
    return get_item_prefix(item_id) == EquipPrefix.Fan.value


def get_body_part_from_item(item_id, gender):
    arr = get_body_part_arr_from_item(item_id, gender)
    return arr[0] if len(arr) > 0 else 0


def get_body_part_arr_from_item(item_id, gender_arg):
    gender = get_gender_from_id(item_id)
    eqp_prefix = equip_prefix.get_equip_prefix_by_val(int(get_item_prefix(item_id)))
    body_part_list = []

    if eqp_prefix != EquipPrefix.Emblem and \
            eqp_prefix != EquipPrefix.Bit and \
            gender != 2 and \
            gender_arg != 2 and gender != gender_arg:
        return body_part_list

    if eqp_prefix is not None:
        if eqp_prefix == EquipPrefix.Hat:
            body_part_list.append(BodyPart.Hat.value)
            body_part_list.append(BodyPart.EvanHat.value)
            body_part_list.append(BodyPart.APHat.value)
            body_part_list.append(BodyPart.DUHat.value)
            body_part_list.append(BodyPart.ZeroHat.value)
        elif eqp_prefix == EquipPrefix.FaceAccessory:
            body_part_list.append(BodyPart.FaceAccessory.value)
            body_part_list.append(BodyPart.APFaceAccessory.value)
            body_part_list.append(BodyPart.DUFaceAccessory.value)
            body_part_list.append(BodyPart.ZeroFaceAccessory.value)
        elif eqp_prefix == EquipPrefix.EyeAccessory:
            body_part_list.append(BodyPart.FaceAccessory.value)
            body_part_list.append(BodyPart.ZeroEyeAccessory.value)
        elif eqp_prefix == EquipPrefix.Earrings:
            body_part_list.append(BodyPart.Earrings.value)
            body_part_list.append(BodyPart.ZeroEarrings.value)
        elif eqp_prefix == EquipPrefix.Top or eqp_prefix == EquipPrefix.Overall:
            body_part_list.append(BodyPart.Top.value)
            body_part_list.append(BodyPart.APTop.value)
            body_part_list.append(BodyPart.DUTop.value)
            body_part_list.append(BodyPart.ZeroTop.value)
        elif eqp_prefix == EquipPrefix.Bottom:
            body_part_list.append(BodyPart.Bottom.value)
            body_part_list.append(BodyPart.APBottom.value)
            body_part_list.append(BodyPart.ZeroBottom.value)
        elif eqp_prefix == EquipPrefix.Shoes:
            body_part_list.append(BodyPart.Shoes.value)
            body_part_list.append(BodyPart.APShoes.value)
            body_part_list.append(BodyPart.ZeroShoes.value)
        elif eqp_prefix == EquipPrefix.Gloves:
            body_part_list.append(BodyPart.Gloves.value)
            body_part_list.append(BodyPart.APGloves.value)
            body_part_list.append(BodyPart.DUGloves.value)
            body_part_list.append(BodyPart.ZeroGloves.value)
        elif eqp_prefix == EquipPrefix.Shield or \
                eqp_prefix == EquipPrefix.Katara or \
                eqp_prefix == EquipPrefix.SecondaryWeapon or \
                eqp_prefix == EquipPrefix.Lapis:
            body_part_list.append(BodyPart.Shield.value)
        elif eqp_prefix == EquipPrefix.Lazuli:
            body_part_list.append(BodyPart.Weapon.value)
        elif eqp_prefix == EquipPrefix.Cape:
            body_part_list.append(BodyPart.Cape.value)
            body_part_list.append(BodyPart.APCape.value)
            body_part_list.append(BodyPart.DUCape.value)
            body_part_list.append(BodyPart.ZeroCape.value)
        elif eqp_prefix == EquipPrefix.Ring:
            body_part_list.append(BodyPart.Ring1.value)
            body_part_list.append(BodyPart.Ring2.value)
            body_part_list.append(BodyPart.Ring3.value)
            body_part_list.append(BodyPart.Ring4.value)
            body_part_list.append(BodyPart.ZeroRing1.value)
            body_part_list.append(BodyPart.ZeroRing2.value)
        elif eqp_prefix == EquipPrefix.Pendant:
            body_part_list.append(BodyPart.Pendant.value)
            body_part_list.append(BodyPart.ExtendedPendant.value)
        elif eqp_prefix == EquipPrefix.Belt:
            body_part_list.append(BodyPart.Belt.value)
        elif eqp_prefix == EquipPrefix.Medal:
            body_part_list.append(BodyPart.Medal.value)
        elif eqp_prefix == EquipPrefix.Shoulder:
            body_part_list.append(BodyPart.Shoulder.value)
        elif eqp_prefix == EquipPrefix.PocketItem:
            body_part_list.append(BodyPart.PocketItem.value)
        elif eqp_prefix == EquipPrefix.MonsterBook:
            body_part_list.append(BodyPart.MonsterBook.value)
        elif eqp_prefix == EquipPrefix.Badge:
            body_part_list.append(BodyPart.Badge.value)
        elif eqp_prefix == EquipPrefix.Emblem:
            body_part_list.append(BodyPart.Emblem.value)
        elif eqp_prefix == EquipPrefix.Totem:
            body_part_list.append(BodyPart.Totem1.value)
            body_part_list.append(BodyPart.Totem2.value)
            body_part_list.append(BodyPart.Totem3.value)
        elif eqp_prefix == EquipPrefix.MachineEngine:
            body_part_list.append(BodyPart.MachineEngine.value)
        elif eqp_prefix == EquipPrefix.MachineArm:
            body_part_list.append(BodyPart.MachineArm.value)
        elif eqp_prefix == EquipPrefix.MachineLeg:
            body_part_list.append(BodyPart.MachineLeg.value)
        elif eqp_prefix == EquipPrefix.MachineFrame:
            body_part_list.append(BodyPart.MachineFrame.value)
        elif eqp_prefix == EquipPrefix.MachineTransistor:
            body_part_list.append(BodyPart.MachineTransistor.value)
        elif eqp_prefix == EquipPrefix.Android:
            body_part_list.append(BodyPart.Android.value)
        elif eqp_prefix == EquipPrefix.MechanicalHeart:
            body_part_list.append(BodyPart.MechanicalHeart.value)
        elif eqp_prefix == EquipPrefix.Bit:
            bit_id = BodyPart.BitsBase.value
            while bit_id <= BodyPart.BitsEnd.value:
                body_part_list.append(bit_id)
                bit_id += 1
        elif eqp_prefix == EquipPrefix.PetWear:
            body_part_list.append(BodyPart.PetWear1.value)
            body_part_list.append(BodyPart.PetWear2.value)
            body_part_list.append(BodyPart.PetWear3.value)
        elif eqp_prefix == EquipPrefix.TamingMob:
            body_part_list.append(BodyPart.TamingMob.value)
        elif eqp_prefix == EquipPrefix.Saddle:
            body_part_list.append(BodyPart.Saddle.value)
        elif eqp_prefix == EquipPrefix.EvanHat:
            body_part_list.append(BodyPart.EvanHat.value)
        elif eqp_prefix == EquipPrefix.EvanPendant:
            body_part_list.append(BodyPart.EvanPendant.value)
        elif eqp_prefix == EquipPrefix.EvanWing:
            body_part_list.append(BodyPart.EvanWing.value)
        elif eqp_prefix == EquipPrefix.EvanShoes:
            body_part_list.append(BodyPart.EvanShoes.value)
        else:
            if is_long_or_big_sword(item_id) or is_weapon(item_id):
                body_part_list.append(BodyPart.Weapon.value)
                if is_fan(item_id):
                    body_part_list.append(BodyPart.HakuFan.value)
                else:
                    body_part_list.append(BodyPart.ZeroWeapon.value)
            else:
                debug.logs(f"Unknown type item id: {item_id}")
    else:
        debug.logs(f"Unknown type item id: {item_id}")

    return body_part_list
