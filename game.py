import math
import random
from network import Network
import pygame
import tkinter as tk
from tkinter import messagebox
from snake import snake
from cube import cube

class Game:
    def __init__(self):
        self.net = Network()

    def drawGrid(self, w, rows, surface):
        sizeBtwn = w
        x = 0
        y = 0
        for i in range(rows):
            x = x + sizeBtwn
            y = y + sizeBtwn

            pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
            pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

    def redrawWindow(self, surface):
        global rows, width, s, snacks
        surface.fill((0, 0, 0))
        s.draw(surface)
        for snack in snacks:
             snack.draw(surface)
        self.drawGrid(width, rows, surface)
        pygame.display.update()

    def randomSnack(self, rows, item):
        positions = item.body

        while True:
            x = random.randrange(rows)
            y = random.randrange(rows)
            if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
                continue
            else:
                break

        return (x, y)

    def message_box(self, subject, content):
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        messagebox.showinfo(subject, content)
        try:
            root.destroy()
        except:
            pass

    def send_data(self, pos_x, pos_y, score):
        data = str(self.net.id) + ":" + str(pos_x) + \
            "," + str(pos_y) + ":" + str(score)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0, 0

    def run(self):
        global width, rows, s, snacks
        while True:
            snake_received_data = self.net.receive()
            snake_color, snake_pos = snake_received_data.split(";",1)
            r,g,b = snake_color.replace("(","").replace(")","").split(",",2)
            x,y = snake_pos.replace("(","").replace(")","").split(",",1)

            player_snake = snake((int(r),int(g),int(b)),(int(x),int(y)))
            s = player_snake
            width = 500
            rows = 20
            win = pygame.display.set_mode((width, width))
            snacks = []
            snacks.append(cube(self.randomSnack(rows, s), color=(0, 255, 0)))
            flag = True
            score = 0
            clock = pygame.time.Clock()

            while flag:
                pygame.time.delay(50)
                clock.tick(10)

                s.dirnx, s.dirny = self.parse_data(
                    self.send_data(s.dirnx, s.dirny, score))
                s.move()

                for snack in snacks:
                    if s.body[0].pos == snack.pos:
                        s.addCube()
                        score += 1
                        snacks.remove(snack)
                        snacks.append(
                            cube(self.randomSnack(rows, s), color=(0, 255, 0)))

                self.send_data(s.dirnx, s.dirny, score)

                for x in range(len(s.body)):
                    if s.body[x].pos in list(map(lambda z: z.pos, s.body[x+1:])):
                        print('Score: ', len(s.body) - 2)
                        self.message_box('You Lost!', 'Play again...')
                        score = 0
                        s.reset((10, 10))
                        break

                self.redrawWindow(win)
        pass
