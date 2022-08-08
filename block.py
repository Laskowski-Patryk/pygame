import random
import pygame


class Block:

    def __init__(self, screen, x, y):
        self.screen = screen
        self.width = 100
        self.height = 30
        self.ability = 1 if random.randint(0, 20) == 1 else 0
        self.x = x
        self.color = (0, 0, 0)
        self.y = y

    def draw(self):
        # if self.ability == 0:
        #     color = (0, 0, 0)
        # else:
        #     color = (255, 0, 0)
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))
