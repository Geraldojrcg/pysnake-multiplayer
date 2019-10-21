import json

class Player(object):
    def __init__(self, ip, score, snake):
        self.ip = ip
        self.score = score
        self.snake = snake

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def json(self):
        return json.dumps(self, default=lambda x: x.__dict__)