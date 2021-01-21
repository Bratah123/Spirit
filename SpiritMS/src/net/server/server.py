import signal
from asyncio import get_event_loop

from src.net.connections.logins.login_server import LoginServer
from src.net.debug import debug


class ServerApp:

    def __init__(self):
        self.name = "ServerApp"
        self._loop = get_event_loop()
        self._clients = []

        self.logged_in = []

        self.login = None
        self.shop = None

    @classmethod
    def run(cls):
        self = ServerApp()

        loop = self._loop

        try:
            loop.add_signal_handler(signal.SIGINT, loop.stop)
            loop.add_signal_handler(signal.SIGTERM, loop.stop)
        except NotImplementedError:
            pass

        def stop_loop_on_completion(f):
            loop.stop()

        future = loop.create_task(self.start())

        try:
            loop.run_forever()

        except KeyboardInterrupt:
            debug.warn(f"{self.name} Received signal to terminate event loop")

        finally:
            future.remove_done_callback(stop_loop_on_completion)
            loop.run_until_complete(loop.shutdown_asyncgens())
            debug.warn(f"Closed {self.name}")

    async def start(self):
        print("Initializing Server...")

        self.login = await LoginServer.run(self)


if __name__ == '__main__':
    loop = get_event_loop()
    ServerApp.run()
