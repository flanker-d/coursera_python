#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __add__(self, other):
        return Vec2d(self._x + other._x, self._y + other._y)

    def __sub__(self, other):
        return Vec2d(self._x - other._x, self._y - other._y)

    def __mul__(self, value):
        return Vec2d(self._x * value, self._y * value)

    def __len__(self):
        return math.sqrt(self._x**2 + self._y**2)

    def int_pair(self):
        return int(self._x), int(self._y)


class SpeedVec2d(Vec2d):
    def __init__(self, x, y):
        super().__init__(x, y)
        self._speed_x = random.random() * 2
        self._speed_y = random.random() * 2

    def get_new_point(self):
        new_point = Vec2d(self._x, self._y) + Vec2d(self._speed_x, self._speed_y)
        self._x = new_point._x
        self._y = new_point._y
        if new_point._x > SCREEN_DIM[0] or new_point._x < 0:
            self._speed_x = -self._speed_x
        if new_point._y > SCREEN_DIM[1] or new_point._y < 0:
            self._speed_y = -self._speed_y
        return self


class Polyline:
    def __init__(self, game_display):
        self._game_display = game_display

    def set_points(self, points):
        """функция перерасчета координат опорных точек"""
        for p in range(len(points)):
            points[p] = points[p].get_new_point()

    def draw_points(self, points, style="points", width=3, color=(255, 255, 255)):
        """функция отрисовки точек на экране"""
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(self._game_display, color,
                                 (int(points[p_n]._x), int(points[p_n]._y)),
                                 (int(points[p_n + 1]._x), int(points[p_n + 1]._y)), width)

        elif style == "points":
            for p in points:
                pygame.draw.circle(self._game_display, color,
                                   (int(p._x), int(p._y)), width)

class Knot(Polyline):
    @staticmethod
    def get_knot(points, steps):
        if len(points) < 3:
            return []
        res = []
        r = range(-2, len(points) - 2)
        for i in r:
            ptn = []
            p1 = (points[i] + points[i + 1]) * 0.5
            p2 = points[i + 1]
            p3 = (points[i + 1] + points[i + 2]) * 0.5
            ptn.append(p1)
            ptn.append(p2)
            ptn.append(p3)

            res.extend(Knot.get_points(ptn, steps))
        return res

    @staticmethod
    def get_point(points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return ((points[deg] * alpha) + Knot.get_point(points, alpha, deg - 1) * (1 - alpha))

    @staticmethod
    def get_points(base_points, steps):
        alpha = 1 / steps
        res = []
        for i in range(steps):
            res.append(Knot.get_point(base_points, i * alpha))
        return res


class Game:
    def __init__(self):
        self._pygame = pygame
        self._pygame.init()
        self._gameDisplay = self._pygame.display.set_mode(SCREEN_DIM)
        self._pygame.display.set_caption("MyScreenSaver")

        self._steps = 35
        self._working = True
        self._show_help = False
        self._pause = True

        self._points = []

        self._hue = 0
        self._color = pygame.Color(0)

        self._polyline = Polyline(self._gameDisplay)
        self._knot = Knot(self._gameDisplay)

    def _draw_help(self):
        """функция отрисовки экрана справки программы"""
        self._gameDisplay.fill((50, 50, 50))
        font1 = self._pygame.font.SysFont("courier", 24)
        font2 = self._pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        data.append(["Num+", "More points"])
        data.append(["Num-", "Less points"])
        data.append(["", ""])
        data.append([str(self._steps), "Current points"])

        self._pygame.draw.lines(self._gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self._gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self._gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

    def _process_event(self, event):
        if event.type == self._pygame.QUIT:
            self._working = False
        if event.type == self._pygame.KEYDOWN:
            if event.key == self._pygame.K_ESCAPE:
                self._working = False
            if event.key == self._pygame.K_r:
                self._points = []
            if event.key == self._pygame.K_p:
                self._pause = not self._pause
            if event.key == pygame.K_KP_PLUS:
                self._steps += 1
            if event.key == pygame.K_F1:
                self._show_help = not self._show_help
            if event.key == pygame.K_KP_MINUS:
                self._steps -= 1 if self._steps > 1 else 0

        if event.type == self._pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            point = SpeedVec2d(x, y)
            self._points.append(point)


    def run(self):
        while self._working:
            for event in self._pygame.event.get():
                self._process_event(event)

            self._gameDisplay.fill((0, 0, 0))
            self._hue = (self._hue + 1) % 360
            self._color.hsla = (self._hue, 100, 50, 100)

            self._polyline.draw_points(self._points)
            self._knot.draw_points(Knot.get_knot(self._points, self._steps), "line", 3, self._color)

            if not self._pause:
                self._polyline.set_points(self._points)
            if self._show_help:
                self._draw_help()

            self._pygame.display.flip()

    def exit(self):
        self._pygame.display.quit()
        self._pygame.quit()
        exit(0)


# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    game = Game()
    game.run()
    game.exit()
