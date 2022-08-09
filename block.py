import random
import pygame
from loot import Loot


class Block:

    def __init__(self, screen, x, y, player):
        self.screen = screen
        self.width = 100
        self.height = 30
        self.ability = 1 if random.randint(0, 20) == 1 else 0
        self.x = x
        self.color = (0, 0, 0)
        self.y = y
        self.player = player

    def draw(self):
        if self.ability == 0:
            self.color = (0, 0, 0)
        else:
            self.color = (0, 255, 0)
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

    def droploot(self):
        if self.ability == 1:
            self.player.loot.append(Loot(self.screen, self.x + self.width / 2, self.y + self.height / 2, self.player))

