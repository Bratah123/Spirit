import socket
from threading import Thread


class SocketClient:
    HOST = "127.0.0.1"
    PORT = 8484
    srv = (HOST, PORT)

    def __init__(self):
        self.buffer = 512
        self.messages = []
        self.client_socket = socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.srv)
        self.receive_thread = Thread(target=self.receive_msg)
        self.receive_thread.start()

    def receive_msg(self):
        while True:
            try:
                msg = self.client_socket.recv(self.buffer).decode()
                print(msg)
            except Exception as e:
                print("[ERROR]", e)
                break

    def send_message(self, message):
        self.client_socket.send(bytes(message, "utf-8"))
        self.messages.append(message)
        if message == "!quit":
            self.client_socket.close()

    def write(self, packet):
        self.client_socket.write(packet)
