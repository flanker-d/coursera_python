#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math
from dataclasses import dataclass


@dataclass
class Point:
    x: float = 0.0
    y: float = 0.0


class Points(Point):
    def __init__(self, x=0, y=0):
        super(Points, self).__init__(x, y)

        self.points = []

    def append(self, c):
        self.points.append(c)


class Vec2d(Points):
    def __init__(self, x=0, y=0):
        super(Vec2d, self).__init__(x, y)
        if isinstance(x, tuple):
            self.x = x[0]
            self.y = x[1]

    def __add__(self, obj):
        return Vec2d(self.x + obj.x, self.y + obj.y)

    def __sub__(self, obj):
        return Vec2d(self.x - obj.x, self.y - obj.y)

    def __mul__(self, k):
        return Vec2d(self.x * k, self.y * k)

    def __len__(self):
        return round(math.sqrt(self.x * self.x + self.y * self.y))  # Return the length in pixels

    def int_pair(self):
        return int(self.x), int(self.y)


class Polyline:
    def __init__(self):
        self.points = []
        self.speeds = []

    def attach_point(self, coord, speed):
        self.points.append(coord)
        self.speeds.append(speed)

    def set_points(self, screen_dim):

        for p in range(len(self.points)):
            self.points[p] += self.speeds[p]
            if self.points[p].x > screen_dim[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(- self.speeds[p].x, self.speeds[p].y)
            if self.points[p].y > screen_dim[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)

    def draw_points(self, context, point, width=3, color=(255, 255, 255)):

        for p in point:
            pygame.draw.circle(context, color, p.int_pair(), width)


class Knot(Polyline):
    def __init__(self, steps):
        super().__init__()
        self.steps = steps

    def attach_point(self, coord, speed):
        super().attach_point(coord, speed)
        self.get_knot()

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg] * alpha) + (self.get_point(points, alpha, deg - 1) * (1 - alpha))

    def get_points(self, base_points):
        alpha = 1 / self.steps
        res = []
        for i in range(self.steps):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def set_points(self, screen_dim):
        super().set_points(screen_dim)
        self.get_knot()

    def draw_points(self, context, points, width=3, color=(255, 255, 255)):
        for p in range(-1, len(points) - 1):
            pygame.draw.line(context, color, points[p].int_pair(), points[p + 1].int_pair(), width)

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
            res.extend(self.get_points(ptn))
        return res


class Game:
    SCREEN_DIM = (800, 600)

    def __init__(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode(self.SCREEN_DIM)
        pygame.display.set_caption("MyScreenSaver")
        self.steps = 5
        self.color = pygame.Color(0)
        self.hue = 0
        self._pause = True
        self._show_help = False
        self.poly_line = Polyline()
        self.saver_line = Knot(self.steps)

    def draw_help(self):

        self.gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        data.append(["Num+", "More points"])
        data.append(["Num-", "Less points"])
        data.append(["", ""])
        data.append([str(self.saver_line.steps), "Current points"])

        pygame.draw.lines(self.gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

    def re_draw(self, show_help):
        self.gameDisplay.fill((0, 0, 0))
        self.hue = (self.hue + 1) % 360
        self.color.hsla = (self.hue, 100, 50, 100)

        self.poly_line.draw_points(self.gameDisplay, self.poly_line.points)
        self.saver_line.draw_points(self.gameDisplay, self.saver_line.get_knot(), 3, self.color)

        if not self._pause:
            self.poly_line.set_points(self.SCREEN_DIM)
            self.saver_line.set_points(self.SCREEN_DIM)

        if show_help:
            self.draw_help()

        pygame.display.flip()

    def run(self):
        working = True

        while working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    working = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        working = False
                    if event.key == pygame.K_r:
                        self.poly_line = Polyline()

                    if event.key == pygame.K_p:
                        self._pause = not self._pause
                    if event.key == pygame.K_KP_PLUS:
                        self.saver_line.steps += 1
                    if event.key == pygame.K_F1:
                        self._show_help = not self._show_help
                    if event.key == pygame.K_KP_MINUS:
                        self.saver_line.steps -= 1 if self.saver_line.steps > 1 else 0

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.poly_line.attach_point(Vec2d(event.pos), Vec2d(random.random() * 2, random.random() * 2))
                    self.saver_line.attach_point(Vec2d(event.pos), Vec2d(random.random() * 2, random.random() * 2))

            self.re_draw(self._show_help)

        pygame.display.quit()
        pygame.quit()


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
    exit(0)
