import socket
from _thread import *
import sys
from player import Player
from snake import Snake
import json
from collections import namedtuple

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

players = []

server = '10.7.104.14'
port = 3010
server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(10)
print("Waiting for a connection")

def threaded_client(conn, addr):
    global players

    while True:
        snake_color = (255,0,0)
        snake_pos = (13,10)

        snake = Snake(snake_color, snake_pos, 0, 1)
        player = Player(addr[0], 0, snake)

        if not any(x.ip == addr[0] for x in players):
            players.append(player)

        for p in players:
            p.snake = p.snake.json()
            p = p.json()

        print(str(players))
        conn.send(str.encode(str(players)))

        #conn.send(str.encode(player.json()))

        data = conn.recv(2048)
    
        if not data:
            players.remove(player)
            conn.send(str.encode("bye"))
            break
        else:
            player_receive = json.loads(data.decode("utf-8") , object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            player.score = player_receive.score
            player.snake = player_receive.snake
        
        
    
    print("Connection Closed")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to: ", addr[0])

    start_new_thread(threaded_client, (conn, addr))
