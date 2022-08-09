import pygame
from loot import Loot


class Paddle:

    def __init__(self, screen, player):
        self.screen = screen
        self.y_pos = self.screen.get_width() - 300
        self.width = 150
        self.height = 25
        self.player = player
        self.x = 500

    def redraw(self):
        rectangle = pygame.Rect(self.x, self.y_pos, self.width, self.height)
        pygame.draw.rect(self.screen, (0, 0, 0), rectangle)

    def move(self, x):
        if x < 0 and self.get_pos() > 0:
            self.x += x
        elif x > 0 and self.get_pos() + self.get_width() < self.screen.get_width():
            self.x += x
        return self.collect()

    def collect(self):
        points = 0
        for loot in self.player.loot:
            if self.x + self.width >= loot.x >= self.x:
                if self.y_pos + self.height >= loot.y >= self.y_pos:
                    loot.collected = 1
                    points += 30
        return points

    def get_pos(self):
        return self.x

    def get_width(self):
        return self.width

    def self_height(self):
        return self.height()
