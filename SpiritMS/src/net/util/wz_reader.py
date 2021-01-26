import os
from xml.etree import ElementTree

WZ_DIR_NAME = "WZ"


async def get_equip_info(equip_id, equip_category):
    """
    Returns a dictionary of all the item stats stored in the xml wz file give an equip id
    Parameters
    ----------
    equip_id: int
    equip_category: str

    -------

    """
    xml_file_name = f"0{str(equip_id)}.img.xml"
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    file_path = f"{root_dir}/{WZ_DIR_NAME}/Character.wz/{equip_category}/{xml_file_name}"
    try:
        dom = ElementTree.parse(file_path)
    except Exception:
        return None
    item_info = dom.getroot()[0]
    item_stats = {}

    for element in item_info:
        item_stats[element.attrib['name']] = element.attrib.get('value')

    return item_stats


async def get_weapon_info(equip_id):
    return await get_equip_info(equip_id, "Weapon")
