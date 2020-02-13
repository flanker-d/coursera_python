#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Help:

    @staticmethod
    def draw_help():
        """функция отрисовки экрана справки программы"""
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
        data.append([str(steps), "Current points"])

        pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


class Vec2d:

    def __init__(self, point):
        self.point = point

    def __add__(self, y):
        """возвращает сумму двух векторов"""
        vector = self.point[0] + y.point[0], self.point[1] + y.point[1]
        return Vec2d(vector)

    def __sub__(self, y):
        """"возвращает разность двух векторов"""
        return self.point[0] - y.point[0], self.point[1] - y.point[1]

    def __mul__(self, k):
        """возвращает произведение вектора на число"""
        vector = self.point[0] * k, self.point[1] * k
        return Vec2d(vector)

    @staticmethod
    def length(x):
        """возвращает длину вектора"""
        return math.sqrt(x.point[0] * x.point[0] + x.point[1] * x.point[1])

    def vec(self, y):
        """возвращает пару координат, определяющих вектор (координаты точки конца вектора),
        координаты начальной точки вектора совпадают с началом системы координат (0, 0)"""
        return y - self.point

    def int_pair(self):
        return self.point


class Polyline:

    def __init__(self, points):
        self.points = points

    def set_points(self, speeds):
        """функция перерасчета координат опорных точек"""
        for p in range(len(self.points)):
            # print(self.points[p].point, point[1])
            self.points[p] = self.points[p] + speeds[p]
            point = self.points[p].point
            speed = speeds[p].point
            if point[0] > SCREEN_DIM[0] or point[0] < 0:
                vector = (- speed[0], speed[1])
                speeds[p] = Vec2d(vector)
            if point[1] > SCREEN_DIM[1] or point[1] < 0:
                vector = (speed[0], -speed[1])
                speeds[p] = Vec2d(vector)

    @staticmethod
    def draw_points(points, style="points", width=3, color=(255, 255, 255)):
        """функция отрисовки точек на экране"""
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                point = points[p_n].point
                point_next = points[p_n + 1].point
                pygame.draw.line(gameDisplay, color,
                                 (int(point[0]), int(point[1])),
                                 (int(point_next[0]), int(point_next[1])), width)

        elif style == "points":
            for p in points:
                pygame.draw.circle(gameDisplay, color,
                                   (int(p.point[0]), int(p.point[1])), width)


class Knot(Polyline):

    def get_knot(self, count):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
            res.extend(self.get_points(ptn, count))
        return res

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)


# =======================================================================================
# Основная программа
# =======================================================================================

if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    points = []
    speeds = []
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
                    points = []
                    speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                point = Vec2d(event.pos)
                points.append(point)
                speed = Vec2d((random.random() * 2, random.random() * 2))
                speeds.append(speed)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        polyline = Polyline(points)
        polyline.draw_points(points)
        knot = Knot(points)
        polyline.draw_points(knot.get_knot(steps), "line", 3, color)
        if not pause:
            polyline.set_points(speeds)
        if show_help:
            Help.draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
