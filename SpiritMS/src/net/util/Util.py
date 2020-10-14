"""
Makes an array of bytes string readable
Params: byte_arr : byte[]
"""


def readable_byte_arr(byte_arr):
    str_to_ret = ""
    for b in byte_arr:
        str_to_ret += "{}02X".format(b)

    return str(str_to_ret)


def to_string(bytes_):
    return ' '.join(
        [bytes_.hex()[i:i+2].upper() for i in range(0, len(bytes_.hex()), 2)])
