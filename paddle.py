import pygame


class Paddle:

    def __init__(self, screen):
        self.screen = screen
        self.y_pos = self.screen.get_width() - 300
        self.width = 150
        self.height = 25
        self.x = 500

    def redraw(self):
        rectangle = pygame.Rect(self.x, self.y_pos, self.width, self.height)
        pygame.draw.rect(self.screen, (0, 0, 0), rectangle)

    def move(self, x):
        self.x = x

    def get_pos(self):
        return self.x

    def get_width(self):
        return self.width

    def self_height(self):
        return self.height()
