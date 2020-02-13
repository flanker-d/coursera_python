#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600) # размеры игрового окна

class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        """возвращает сумму двух векторов
        """
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """возвращает разность двух векторов
        """
        return Vec2d(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """возвращает произведение вектора на число
        """
        return Vec2d(self.x * other, self.y * other)

    def len(self):
        """возвращает длину вектора
        """
        return math.sqrt(self.x**2 + self.y**2)

    def int_pair(self):
        """возвращает пару координат, определяющих вектор (координаты точки конца вектора)
        """
        return int(self.x), int(self.y)



class Polyline:
    """класс замкнутых ломаных
    """
    def __init__(self, steps=35):
        self.points = []
        self.speeds = []
        self.steps=steps
        self.knots = []

    def add_point(self, point):
        self.points.append(Vec2d(point[0], point[1]))
        self.speeds.append(Vec2d(random.random() * 2, random.random() * 2))

    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            if len(self.points) >= 3:
                for p in range(-3, len(self.knots) - 1):
                    pygame.draw.line(gameDisplay, color,
                                     self.knots[p].int_pair(),
                                     self.knots[p + 1].int_pair(), width)

        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color,
                                   p.int_pair(), width)


class Knot(Polyline):
    """класс Knot
    """

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg] * alpha
                + self.get_point(points, alpha, deg - 1) * (1 - alpha))

    def get_points(self, base_points):
        alpha = 1 / self.steps
        res = []
        for i in range(self.steps):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        """Расчет координат кривых
        """
        if len(self.points) < 3:
            return []
        self.knots.clear()
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
            self.knots.extend(self.get_points(ptn))
        return self.knots

    def set_points(self):
        """Coordinates recalculation for polyline moving."""
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p].x = -self.speeds[p].x
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p].y = -self.speeds[p].y


def draw_help():
    """функция отрисовки экрана справки программы
    """
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([str(knot.steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))



if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    working = True   
    knot = Knot()
    show_help = False
    pause = True
    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    knot = Knot()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    knot.steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    knot.steps -= 1 if knot.steps > 1 else 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                knot.add_point(event.pos)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        
        knot.draw_points()
        knot.get_knot()
        knot.draw_points("line", 3, color)
        if not pause:
            knot.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
