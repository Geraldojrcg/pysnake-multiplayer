import socket
from _thread import *
import sys


class Player(object):
    def __init__(self, ip, pos_x, pos_y, score):
        self.ip = ip
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.score = score

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

players = []

server = 'localhost'
port = 8080

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(10)
print("Waiting for a connection")

currentId = "0"
pos = ["0:50,50", "1:100,100"]


def threaded_client(conn, addr):
    global currentId, pos, players
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            player = Player(addr[0], reply.split(":")[1].split(",")[0], reply.split(":")[1].split(",")[1], reply.split(":")[2])
            flag = False
            for player in players:
                if player.ip == addr[0]:
                    flag = True
            if not flag:
                players.append(player)
        
            if not data:
                players.remove(player)
                conn.send(str.encode("bye"))
                break
            else:
                player.score = reply.split(":")[2]
                player.pos_x = reply.split(":")[1].split(",")[0]
                player.pos_y = reply.split(":")[1].split(",")[1]

            print(players)

            conn.sendall(str.encode(reply))
        except:
            break
    
    print("Connection Closed")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to: ", addr[0])

    start_new_thread(threaded_client, (conn, addr))
