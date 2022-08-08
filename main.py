import pygame
from paddle import Paddle
from ball import Ball
from block import Block
import time
import numpy as np

window_height = 800
window_width = 1000
pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('My_game')
pygame.display.flip()
clock = pygame.time.Clock()
done = False
frame_cap = 1.0 / 160
time_1 = time.perf_counter()
unprocessed = 0
padd = Paddle(screen)
balls = []
blocks = []
startgame = 0
pygame.font.init()
points = 0
my_font = pygame.font.SysFont('Comic Sans MS', 30)
i = 0

for x in range(50, window_width - 100, 160):
    for y in range(25, int(window_height / 3), 50):
        blocks.append(Block(screen, x, y))

def checkwin():
    if len(blocks) == 0:
        startgame = 0
        text_surface = my_font.render('ZDOBYŁEŚ ' + str(points) + ' PKT, GRATULACJE', False, (0, 0, 0))
        screen.blit(text_surface, (300, 300))
        done = True

    else:
        return 0

while not done:
    can_render = False
    time_2 = time.perf_counter()
    passed = time_2 - time_1
    unprocessed += passed
    time_1 = time_2

    while unprocessed >= frame_cap:
        unprocessed -= frame_cap
        can_render = True

    if can_render:
        screen.fill((255, 255, 12))
        text_surface = my_font.render('Points: ' + str(points), False, (0, 0, 0))

        screen.blit(text_surface, (20, window_height - 50))
        keys = pygame.key.get_pressed()  # checking pressed keys
        if keys[pygame.K_LEFT] and padd.get_pos() > 0:
            padd.move(padd.get_pos() - 3)
        if keys[pygame.K_RIGHT] and padd.get_pos() + padd.get_width() < window_width:
            padd.move(padd.get_pos() + 3)
        if keys[pygame.K_SPACE] and startgame == 0:
            startgame = 1

        for block in blocks:
            block.draw()

        for ball in balls:
            points += ball.redraw(startgame, blocks)
            if ball.checkLose() == 1:
                balls.remove(ball)
        checkwin()
        if len(balls) == 0:
            startgame = 0
            for c in range(50):
                balls.append(Ball(screen, padd, screen.get_width() / 2, screen.get_height() / 2))

        padd.redraw()
        # pygame.image.save(screen, "./screens/screenshot" + str(i) + ".jpg")
        i += 1
        # startgame = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

    pygame.display.flip()



