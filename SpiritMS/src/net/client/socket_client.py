import asyncio

from src.net.packets.byte_buffer.packet import Packet
from src.net.packets.encryption.maple_aes import MapleAes
from src.net.packets.encryption.shanda import Shanda
from src.net.server import server_constants

"""
    Credits go to Rooba for this SocketClient
"""


class SocketClient:
    def __init__(self, socket, riv, siv):
        self._loop = asyncio.get_event_loop()
        self._socket = socket
        self._lock = asyncio.Lock()
        self.receive_size = 16384
        self.riv = riv
        self.siv = siv
        self._r_counter = 0
        self._s_counter = 0
        self._is_online = False
        self._overflow = None

    @property
    def identifier(self):
        return self._socket.getpeername()

    def close(self):
        """
            Regular python socket object close() function
        """
        return self._socket.close()

    async def receive(self, client):
        self._is_online = True
        while self._is_online:
            if not self._overflow:
                recv_buffer = await self._loop.sock_recv(self._socket, self.receive_size)

                if not recv_buffer:
                    client._parent.on_client_disconnect(client)
                    return

            else:
                recv_buffer = self._overflow
                self._overflow = None

            if self.riv:
                async with self._lock:
                    length = MapleAes.get_length(recv_buffer)
                    if length != len(recv_buffer) - 4:
                        self._overflow = recv_buffer[length + 4:]
                        recv_buffer = recv_buffer[:length + 4]
                    recv_buffer = self.manipulate_buffer(recv_buffer)

            client.dispatch(Packet(recv_buffer))

    async def send_packet(self, out_packet):
        packet_length = len(out_packet)
        packet = bytearray(out_packet.getvalue())

        buf = packet[:]

        final_length = packet_length + 4
        final = bytearray(final_length)
        async with self._lock:
            MapleAes.get_header(final, self.siv, packet_length, server_constants.SERVER_VERSION)
            buf = Shanda.encrypt_transform(buf)
            final[4:] = MapleAes.transform(buf, self.siv)

        await self._loop.sock_sendall(self._socket, final)

    async def send_packet_raw(self, packet):
        await self._loop.sock_sendall(self._socket, packet.getvalue())

    def manipulate_buffer(self, buffer):
        buf = bytearray(buffer)[4:]

        buf = MapleAes.transform(buf, self.riv)
        buf = Shanda.decrypt_transform(buf)

        return buf
