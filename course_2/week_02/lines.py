import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:

    # def __init__(self, x, y):
    #     self.x = x
    #     self.y = y

    def add(self, x, y):
        """возвращает сумму двух векторов"""
        return x[0] + y[0], x[1] + y[1]
    # x[0] and x[1] - 1st vector, y[0] and y[1] - 2nd vector

    # adding two objects
    # def __add__(self, v):
    #     new_x = self.x + v.x
    #     new_y = self.y + v.y
    #
    #     return Vec2d(new_x, new_y)


    def length(self, x):
        """возвращает длину вектора"""
        return math.sqrt(x[0] * x[0] + x[1] * x[1])

    def mul(self, v, k):
        """возвращает произведение вектора на число"""
        return v[0] * k, v[1] * k

    def vec(self, x, y):
        """возвращает пару координат, определяющих вектор (координаты точки конца вектора),
        координаты начальной точки вектора совпадают с началом системы координат (0, 0)"""
        return self.sub(y, x)

    def sub(self, x, y):
        """"возвращает разность двух векторов"""
        return x[0] - y[0], x[1] - y[1]


class Polyline:

    def set_points(self, points, speeds):
        """функция перерасчета координат опорных точек"""
        for p in range(len(points)):
            vec2d = Vec2d()
            points[p] = vec2d.add(points[p], speeds[p])
            if points[p][0] > SCREEN_DIM[0] or points[p][0] < 0:
                speeds[p] = (- speeds[p][0], speeds[p][1])
            if points[p][1] > SCREEN_DIM[1] or points[p][1] < 0:
                speeds[p] = (speeds[p][0], -speeds[p][1])

    def draw_points(self, points, style="points", width=3, color=(255, 255, 255)):
        """функция отрисовки точек на экране"""
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color,
                                 (int(points[p_n][0]), int(points[p_n][1])),
                                 (int(points[p_n + 1][0]), int(points[p_n + 1][1])), width)

        elif style == "points":
            for p in points:
                pygame.draw.circle(gameDisplay, color,
                                   (int(p[0]), int(p[1])), width)


class Knot(Polyline):

    def get_knot(self, points, count):
        if len(points) < 3:
            return []
        res = []
        for i in range(-2, len(points) - 2):
            ptn = []
            vec2d = Vec2d()

            ptn.append(vec2d.mul(
                vec2d.add(points[i], points[i + 1]), 0.5
            ))

            ptn.append(points[i + 1])
            ptn.append(vec2d.mul(vec2d.add(points[i + 1], points[i + 2]), 0.5))

            p = Points()
            res.extend(p.get_points(ptn, count))
        return res


class Points:

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

        vec2d = Vec2d()
        return vec2d.add(vec2d.mul(points[deg], alpha), vec2d.mul(self.get_point(points, alpha, deg - 1), 1 - alpha))


class HelpDrawer:

    def draw_help(self):
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
                points.append(event.pos)
                speeds.append((random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)

        #
        # code here
        polyline = Polyline()
        polyline.draw_points(points)
        #

        # draw_points(points)
        knot = Knot()
        p = knot.get_knot(points, steps)
        polyline.draw_points(p, "line", 3, color)

        # draw_points(get_knot(points, steps), "line", 3, color)

        if not pause:
            polyline.set_points(points, speeds)
            # set_points(points, speeds)
        if show_help:
            HelpDrawer().draw_help()
            # draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
