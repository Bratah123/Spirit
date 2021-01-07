import asyncio

from src.net.connections.logins.login_server import LoginServer


async def main():
    server = LoginServer()
    await server.bind_and_listen()


if __name__ == "__main__":
    asyncio.run(main())
