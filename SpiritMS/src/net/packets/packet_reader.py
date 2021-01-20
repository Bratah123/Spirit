from src.net.debug import debug


class PacketReader:
    def __init__(self, parent):
        self.parent = parent

    def push(self, client, packet):
        debug.logs(f"InPacket Opcode: {packet.name}: | {packet.to_string()} |")

        try:
            coro = None

            for packet_handler in self.parent.packet_handlers:
                if packet_handler.opcode == packet.opcode:
                    coro = packet_handler.callback
                    break

            if not coro:
                raise AttributeError

        except AttributeError:
            debug.warn(
                f"{self.parent.name} Unhandled InPacket in : {packet.name}")

        else:
            self.parent._loop.create_task(
                self._run_event(coro, client, packet))

    async def _run_event(self, coro, *args):
        await coro(self.parent, *args)
