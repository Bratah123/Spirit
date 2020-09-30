"""
Makes an array of bytes string readable
Params: byte_arr : byte[]
"""


def readable_byte_arr(byte_arr):
    str_to_ret = ""
    for b in byte_arr:
        str_to_ret += "{}02X".format(b)

    return str(str_to_ret)
