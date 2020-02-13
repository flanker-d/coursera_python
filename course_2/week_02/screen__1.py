#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)


# =======================================================================================
# Основной класс Vec2d
# =======================================================================================
class Vec2d:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __neg__(self):
        """возвращает обратный вектор"""
        return Vec2d(-self.x, -self.y)

    def __add__(self, other):
        """возвращает сумму двух векторов"""
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """возвращает сумму двух векторов"""
        return self + (-other)

    def __mul__(self, k):
        """возвращает произведение вектора на число"""
        return Vec2d(self.x * k, self.y * k)

    def __rmul__(self, k):
        """возвращает произведение вектора на число"""
        return Vec2d(self.x * k, self.y * k)

    def __len__(self):
        """возвращает длину вектора"""
        # кастуем в int, потому что: https://www.coursera.org/learn/oop-patterns-python/peer/BebZd/sozdaniie-iierarkhii-klassov/discussions/threads/euz-yN9fEemb0Q7Qs84AhA
        # Пункт 9
        return int(math.sqrt(self.x * self.x + self.y * self.y))

    def int_pair(self):
        return (self.x, self.y)

    @property
    def length(self):
        """возвращает длину вектора"""
        return math.sqrt(self.x * self.x + self.y * self.y)


# =======================================================================================
# Основной класс Polyline
# =======================================================================================
class Polyline:
    def __init__(self, gameDisplay):
        self.points = []
        self.speeds = []
        self.gameDisplay = gameDisplay

    def add_point(self, point, speed):
        self.points.append(Vec2d(point[0], point[1]))
        self.speeds.append(Vec2d(speed[0], speed[1]))

    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(- self.speeds[p].x, self.speeds[p].y)
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)

    def draw_points(self, width=3, color=(255, 255, 255)):
        for p in self.points:
            pygame.draw.circle(self.gameDisplay, color,
                               (int(p.x), int(p.y)), width)


# =======================================================================================
# Основной класс Knot
# =======================================================================================
class Knot(Polyline):
    def __init__(self, gameDisplay):
        super().__init__(gameDisplay)
        self.ex_points = []

    def draw_points(self, width=3, color=(255, 255, 255), steps=35):
        self.ex_points = self.get_knot(self.points, steps)
        for p_n in range(-1, len(self.ex_points) - 1):
            pygame.draw.line(self.gameDisplay,
                             color,
                             (int(self.ex_points[p_n].x),
                              int(self.ex_points[p_n].y)),
                             (int(self.ex_points[p_n + 1].x),
                              int(self.ex_points[p_n + 1].y)),
                             width)

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self, points, count):
        if len(points) < 3:
            return []
        res = []
        for i in range(-2, len(points) - 2):
            ptn = []
            ptn.append((points[i] + points[i + 1]) * 0.5)
            ptn.append(points[i + 1])
            ptn.append((points[i + 1] + points[i + 2]) * 0.5)

            res.extend(self.get_points(ptn, count))
        return res


# =======================================================================================
# Основной класс Игры
# =======================================================================================
class Game:
    def __init__(self, steps, gameDisplay, color):
        self.steps = steps
        self.gameDisplay = gameDisplay
        self.working = True
        self.show_help = False
        self.pause = True
        self.hue = 0
        self.color = color
        self.poly = Polyline(gameDisplay)
        self.knot = Knot(gameDisplay)

    def init_main_loop(self):
        while self.working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.working = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.working = False
                    if event.key == pygame.K_r:
                        self.poly = Polyline(self.gameDisplay)
                        self.knot = Knot(self.gameDisplay)
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                    if event.key == pygame.K_KP_PLUS:
                        self.steps += 1
                    if event.key == pygame.K_F1:
                        self.show_help = not self.show_help
                    if event.key == pygame.K_KP_MINUS:
                        self.steps -= 1 if self.steps > 1 else 0

                if event.type == pygame.MOUSEBUTTONDOWN:
                    point = event.pos
                    speed = (random.random() * 2, random.random() * 2)

                    self.poly.add_point(point, speed)
                    self.knot.add_point(point, speed)

            self.gameDisplay.fill((0, 0, 0))
            self.hue = (self.hue + 1) % 360
            self.color.hsla = (self.hue, 100, 50, 100)
            self.poly.draw_points()
            self.knot.draw_points(3, self.color, self.steps)

            if not self.pause:
                self.poly.set_points()
                self.knot.set_points()
            if self.show_help:
                self.draw_help()

            pygame.display.flip()

    def draw_help(self):
        """функция отрисовки экрана справки программы"""
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
        data.append([str(self.steps), "Current points"])

        pygame.draw.lines(self.gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# =======================================================================================
# Основная программа
# =======================================================================================
def main():
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")
    color = pygame.Color(0)

    game = Game(35, gameDisplay, color)
    game.init_main_loop()

    pygame.display.quit()
    pygame.quit()
    exit(0)


if __name__ == "__main__":
    main()
