from paddle import Paddle
from ball import Ball
from block import Block
import uuid


class Player:
    def __init__(self, screen):
        self.screen = screen
        self.blocks = []
        self.balls = []
        self.id = uuid.uuid1()
        self.padd = Paddle(self.screen, self)
        self.fillblocks()
        self.fillballs(1)
        self.points = 0
        self.loot = []

    def fillblocks(self):
        if len(self.blocks) == 0:
            for x in range(50, self.screen.get_width() - 100, 160):
                for y in range(25, int(self.screen.get_height() / 3), 50):
                    self.blocks.append(Block(self.screen, x, y, self))

    def fillballs(self, x):
        for i in range(x):
            self.balls.append(Ball(self.screen, self.padd, self.screen.get_width() / 2, self.screen.get_height() / 2))
