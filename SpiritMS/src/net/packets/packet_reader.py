from src.net.debug.debug import Debug


class PacketReader:
    def __init__(self, parent):
        self.parent = parent

    def push(self, client, packet):
        Debug.logs(f"InPacket Opcode: {packet.name}: | {packet.to_string()} |")

        try:
            coro = None

            for packet_handler in self.parent._packet_handlers:
                if packet_handler.op_code == packet.op_code:
                    coro = packet_handler.callback
                    break

            if not coro:
                raise AttributeError

        except AttributeError:
            Debug.warn(
                f"{self.parent.name} Unhandled InPacket in : <w>{packet.name}</w>")

        else:
            self.parent._loop.create_task(
                self._run_event(coro, client, packet))

    async def _run_event(self, coro, *args):
        await coro(self.parent, *args)
