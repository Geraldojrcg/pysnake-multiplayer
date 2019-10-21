class Player(object):
    def __init__(self, ip, pos_x, pos_y, score, snake):
        self.ip = ip
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.score = score
        self.snake = None

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)