import socket
from _thread import *
import sys
from player import Player
from snake import snake

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

players = []

server = '10.7.129.25'
port = 3000
server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(10)
print("Waiting for a connection")

def threaded_client(conn, addr):
    global players
    reply = ''
    snake_color = (255,0,0)
    snake_pos = (13,10)
    conn.send(str.encode(str(snake_color)+";"+str(snake_pos)))
    while True:
        try:
            data = conn.recv(2048)

            reply = data.decode('utf-8')
            player = Player(addr[0], reply.split(":")[1].split(",")[0], reply.split(":")[1].split(",")[1], reply.split(":")[2], None)
            
            if not any(x.ip == addr[0] for x in players):
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
