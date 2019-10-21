import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "10.7.104.14"
        self.port = 3010
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        return self.client.connect(self.addr)

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode("utf-8")
            return reply
        except socket.error as e:
            return str(e)
    
    def receive(self):
        try:
            reply = self.client.recv(2048).decode("utf-8")
            return reply
        except socket.error as e:
            return str(e)
