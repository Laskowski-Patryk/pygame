import pygame


class Loot:
    def __init__(self, screen, x, y, player):
        self.screen = screen
        self.y = y
        self.x = x
        self.points = 5
        self.radius = 10
        self.collected = 0
        self.player = player
        self.player.loot.append(self)

    def draw(self):
        if self.collected == 0:
            pygame.draw.circle(self.screen, (0, 255, 0), (self.x, self.y), self.radius)
            self.y += 1
            return 1
        else:
            self.player.loot.remove(self)
            return 0
