class PacketHandler:

    def __init__(self, name, callback, **kwargs):
        self.name = name
        self.callback = callback
        self.opcode = kwargs.get('opcode')


def packet_handler(opcode=None):
    """
    A decorater that lets just handle InHeaders
    :param opcode: OutPacket
    :return: PacketHandler Class
    """

    def wrap(func):
        return PacketHandler(func.__name__, func, opcode=opcode)

    return wrap
