"""
Makes an array of bytes string readable
Params: byte_arr : byte[]
"""
import json


def readable_byte_arr(byte_arr):
    str_to_ret = ""
    for b in byte_arr:
        str_to_ret += "{}02X".format(b)

    return str(str_to_ret)


def to_string(bytes_):
    # Given bytes represent it as a little endian hex array
    return ' '.join(
        [bytes_.hex()[i:i + 2].upper() for i in range(0, len(bytes_.hex()), 2)])


def print_dict(dictionary):
    # A function that prints out dictionaries neatly
    print(json.dumps(dictionary, indent=4))
