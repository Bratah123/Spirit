from src.net.connections.logins.LoginServer import LoginServer


def main():
    server = LoginServer()
    server.bind_and_listen()


if __name__ == "__main__":
    main()
