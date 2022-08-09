import pygame
import numpy as np
import math
from scipy.interpolate import interp1d
import random

class Ball:

    def __init__(self, screen, padd, x=300, y=400):
        self.padd = padd
        self.screen = screen
        self.speed = float(3)
        self.initial = np.array([float(x), float(y)])
        self.xy = np.array([float(x), float(y)])
        rand = pow(self.speed, 2) + pow(self.speed, 2)
        x = random.randint(1, rand - 1)
        c = math.sqrt(rand - x)
        if random.randint(0, 1) == 1:
            c *= -1
        self.vel = np.array([c, math.sqrt(x)])
        self.radius = 7

    def redraw(self, move, blocks):
        point = 0
        if move == 1:
            if self.move(blocks) == 1:
                point = 1
        pygame.draw.circle(self.screen, (0, 0, 0), self.xy, self.radius)
        return point

    def checkcollision(self, blocks):
        closest = []
        collide = 0
        for block in blocks:
            block.color = (0, 0, 0)
            center = np.array([block.x + 50, block.y + 15])
            temp = np.linalg.norm(self.xy - center)
            closest.append([temp, block])

        closest = sorted(closest, key=lambda x: x[0], reverse=False)

        if len(closest) != 0 and closest[0][0] > 100:
            return collide

        newlist = []
        i = 0
        for cl in closest:
            if i <= 3:
                if cl[0] <= 100:
                    newlist.append(cl[1])
            else:
                break
            i += 1

        tolerance = 3
        for block in newlist:
            # block.color = (0, 255, 0)

            if abs(self.xy[1] - self.radius - (block.y + 30)) <= tolerance:  # top
                if block.x + block.width >= self.xy[0] >= block.x:
                    self.vel[1] = abs(self.vel[1])
                    collide = 1
                    block.droploot()
                    blocks.remove(block)
                    continue

            if abs(self.xy[1] + self.radius - block.y) <= tolerance:  # bottom
                if block.x + block.width >= self.xy[0] >= block.x:
                    self.vel[1] = -abs(self.vel[1])
                    collide = 1
                    block.droploot()
                    blocks.remove(block)
                    continue

            if abs(self.xy[0] - self.radius - (block.x + block.width)) <= tolerance:  # left
                if block.y + 30 >= self.xy[1] >= block.y:
                    self.vel[0] = abs(self.vel[0])
                    collide = 1
                    block.droploot()
                    blocks.remove(block)
                    continue

            if abs(self.xy[0] + self.radius - block.x) <= tolerance:  # right
                if block.y + 30 >= self.xy[1] >= block.y:
                    self.vel[0] = -abs(self.vel[0])
                    collide = 1
                    block.droploot()
                    blocks.remove(block)
                    continue

            a = np.array((block.x + block.width, block.y + 30))  # left up
            b = np.array((self.xy[0] - self.radius / 2, self.xy[1] - self.radius / 2))
            if np.linalg.norm(a - b) <= self.radius:
                if self.xy[0] - self.radius / 2 > block.x + block.width:
                    self.vel[0] = abs(self.vel[0])
                else:
                    self.vel[1] = abs(self.vel[1])
                collide = 1
                block.droploot()
                blocks.remove(block)
                continue

            a = np.array((block.x + block.width, block.y))  # left down
            b = np.array((self.xy[0] - self.radius / 2, self.xy[1] + self.radius / 2))
            if np.linalg.norm(a - b) <= self.radius:
                if self.xy[0] + self.radius / 2 > block.x + block.width:
                    self.vel[0] = abs(self.vel[0])
                else:
                    self.vel[1] = -abs(self.vel[1])
                collide = 1
                block.droploot()
                blocks.remove(block)
                continue

            a = np.array((block.x, block.y))  # right down
            b = np.array((self.xy[0] + self.radius / 2, self.xy[1] + self.radius / 2))
            if np.linalg.norm(a - b) <= self.radius:
                if self.xy[0] + self.radius / 2 > block.x:
                    self.vel[0] = -abs(self.vel[0])
                else:
                    self.vel[1] = -abs(self.vel[1])
                collide = 1
                block.droploot()
                blocks.remove(block)
                continue

            a = np.array((block.x, block.y + 30))  # right up
            b = np.array((self.xy[0] + self.radius / 2, self.xy[1] - self.radius / 2))
            if np.linalg.norm(a - b) <= self.radius:
                if self.xy[0] + self.radius / 2 > block.x:
                    self.vel[1] = abs(self.vel[1])
                else:
                    self.vel[0] = -abs(self.vel[0])
                collide = 1
                block.droploot()
                blocks.remove(block)
                continue

        return collide

    def move(self, blocks):

        self.checkLose()
        point = 0
        if self.checkcollision(blocks) == 1:
            point = 1
        if (self.padd.get_pos() <= self.xy[0] <= (
                self.padd.get_pos() + self.padd.get_width())) and self.padd.y_pos + 25 >= self.xy[
            1] + self.radius >= self.padd.y_pos and self.vel[1] > 0:
            self.vel[1] *= -1
            if self.padd.get_pos() + self.padd.get_width() >= self.xy[
                0] >= self.padd.get_pos() + self.padd.get_width() * 0.75:
                sq = pow(self.vel[0], 2) + pow(self.vel[1], 2)
                m = interp1d(
                    [self.padd.get_pos() + self.padd.get_width(), self.padd.get_pos() + self.padd.get_width() * 0.75],
                    [1, sq - 1])
                v1 = sq - m(self.xy[0])
                v2 = m(self.xy[0])
                v1, v2 = math.sqrt(v1), math.sqrt(v2)
                self.vel = np.array([v1, -v2])

            if self.xy[0] <= self.padd.get_pos() + self.padd.get_width() / 4:
                sq = pow(self.vel[0], 2) + pow(self.vel[1], 2)
                m = interp1d(
                    [self.padd.get_pos(), self.padd.get_pos() + self.padd.get_width() / 4],
                    [1, sq - 1])
                v1 = sq - m(self.xy[0])
                v2 = m(self.xy[0])
                v1, v2 = math.sqrt(v1), math.sqrt(v2)
                self.vel = np.array([-v1, -v2])

        if self.xy[1] - self.radius <= 0:
            self.vel[1] *= -1

        if self.xy[0] - self.radius <= 0:
            self.vel[0] *= -1

        if self.xy[0] + self.radius >= self.screen.get_width():
            self.vel[0] *= -1
        # print(self.xy)
        self.xy += self.vel
        return point

    def checkLose(self):
        if self.xy[1] >= self.screen.get_height():
            self.xy = [self.screen.get_width() / 2, self.screen.get_height() / 2]
            return 1
        else:
            return 0
