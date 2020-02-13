"""
Task screensaver.
Please enter f1 when start.
"""

import pygame
import random
import math


SCREEN_DIM = (800, 600)


class Vec2d:
    def __init__(self, end):
        self.end = end
        self.x = end[0]
        self.y = end[1]

    def __add__(self, other):
        return self.x + other.x, self.y + other.y

    def __sub__(self, other):
        return self.x - other.x, self.y - other.y

    def __mul__(self, other):
        return self.x * other, self.y * other

    def __len__(self):
        return int(math.sqrt(self.x * self.x + self.y * self.y))

    def int_pair(self):
        return int(self.x), int(self.y)


class Polyline:
    def __init__(self, points):
        self.points = points
        self.ball_size = 0

    def set_points(self, points, speeds):
        for p in range(len(points)):
            point = Vec2d(points[p])
            speed = Vec2d(speeds[p])

            points[p] = point + speed
            if points[p][0] > SCREEN_DIM[0] or points[p][0] < 0:
                speeds[p] = (- speeds[p][0], speeds[p][1])
            if points[p][1] > SCREEN_DIM[1] or points[p][1] < 0:
                speeds[p] = (speeds[p][0], -speeds[p][1])

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]

        x = Vec2d(points[deg])
        y = Vec2d(self.get_point(points, alpha, deg - 1))

        x_alpha = Vec2d(x * alpha)
        y_alpha = Vec2d(y * (1 - alpha))

        return x_alpha + y_alpha

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def draw_points(self, points, style="points", width=3, color=(255, 155, 155)):
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color,
                                 (int(points[p_n][0]), int(points[p_n][1])),
                                 (int(points[p_n + 1][0]), int(points[p_n + 1][1])), width)

        elif style == "points":
            for p in points:
                pygame.draw.circle(gameDisplay, color,
                                   (int(p[0]), int(p[1])), width + self.ball_size)

    def draw_help(self):
        gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["D", "Delete point"])
        data.append(["F", "Speed up"])
        data.append(["S", "Speed down"])
        data.append(["C", "Add new curve"])
        data.append(["Up", "Increase ball size"])
        data.append(["Down", "Decrease ball size"])

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


class Knot(Polyline):
    def __init__(self, points):
        super().__init__(points)

    def get_knot(self, points, count):
        if len(points) < 3:
            return []
        res = []
        for i in range(-2, len(points) - 2):
            ptn = []

            first = Vec2d(points[i])
            second = Vec2d(points[i + 1])
            third = Vec2d(points[i + 2])

            ptn.append(Vec2d(first + second) * 0.5)
            ptn.append(points[i + 1])
            ptn.append(Vec2d(second + third) * 0.5)
            res.extend(self.get_points(ptn, count))
        return res



if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    show_help = False
    pause = True
    add_curve = False
    all_points = [[]]
    all_speeds = [[]]

    hue = 0
    color = pygame.Color(0)

    knot = Knot(all_points)
    curve = 0

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

                # For additional functions
                if event.key == pygame.K_d:
                    if len(all_points[-1]) > 0:
                        all_points[-1].pop()
                        all_speeds[-1].pop()

                    else:
                        if len(all_points) > 1:
                            all_points.pop()
                            all_speeds.pop()

                if event.key == pygame.K_f:
                    for i in range(len(all_speeds)):
                        tmp = []
                        for speed in all_speeds[i]:
                            first = speed[0]
                            second = speed[1]
                            if abs(first + first / 4) < 15:
                                first = first + first / 4
                            if abs(second + second / 4) < 8:
                                second = second + second / 4
                            tmp.append((first, second))
                        all_speeds[i] = tmp

                if event.key == pygame.K_s:
                    for i in range(len(all_speeds)):
                        tmp = []
                        for speed in all_speeds[i]:
                            first = speed[0]
                            second = speed[1]
                            if abs(first - first / 5) > 0.05:
                                first = first - first / 5
                            if abs(second - second / 5) > 0.05:
                                second = second - second / 5
                            tmp.append((first, second))
                        all_speeds[i] = tmp
                if event.key == pygame.K_c:
                    add_curve = not add_curve

                if event.key == pygame.K_UP:
                    if knot.ball_size < 16:
                        knot.ball_size += 1

                if event.key == pygame.K_DOWN:
                    if knot.ball_size > 0:
                        knot.ball_size -= 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                all_points[-1].append(event.pos)
                all_speeds[-1].append((random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)

        # For more than one curve
        for i, points in enumerate(all_points):
            knot.draw_points(points)
            knot.draw_points(knot.get_knot(points, steps), "line", 3, color)

        if not pause:
            for i in range(len(all_points)):
                knot.set_points(all_points[i], all_speeds[i])

        if show_help:
            knot.draw_help()

        if add_curve:
            all_points.append([])
            all_speeds.append([])
            add_curve = not add_curve

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
