import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:
    def __init__(self, x, y=None):
        if y is None:
            self.x = x[0]
            self.y = x[1]
        else:
            self.x = x
            self.y = y

    def __add__(self, other):
        """возвращает сумму двух векторов"""
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """возвращает разность двух векторов"""
        return Vec2d(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """возвращает произведение вектора на число"""
        if isinstance(other, Vec2d):
            return self.x * other.x + self.y * other.y
        else:
            return Vec2d(self.x * other, self.y * other)

    def __len__(self, x):
        """возвращает длину вектора"""
        return math.sqrt(x.x ** 2 + x.y ** 2)

    def int_pair(self):
        return (int(self.x), int(self.y))


class Polyline:
    def __init__(self):
        self.points = []
        self.speeds = []

    def __len__(self):
        return len(self.points)

    def __str__(self):
        return str(self.points), str(self.speeds)

    def __delete__(self, num=None):
        if num is None:
            self.points.pop()
            self.speeds.pop()
        else:
            self.points.pop(num)
            self.speeds.pop(num)

    def add_point(self, point, speed):
        self.points.append(point)
        self.speeds.append(speed)

    def delete_point(self):
        self.__delete__()

    def set_points(self):
        """функция перерасчета координат опорных точек"""
        for index in range(len(self.points)):
            self.points[index] += self.speeds[index]

            if self.points[index].x > SCREEN_DIM[0] or self.points[index].x < 0:
                self.speeds[index] = Vec2d(- self.speeds[index].x, self.speeds[index].y)

            if self.points[index].y > SCREEN_DIM[1] or self.points[index].y < 0:
                self.speeds[index] = Vec2d(self.speeds[index].x, -self.speeds[index].y)

    def draw_points(self, points, width=3, color=(255, 255, 255)):
        """функция отрисовки ломаной"""
        for point in points:
            pygame.draw.circle(gameDisplay, color, point.int_pair(), width)

    def increase_speed(self):
        for point in range(len(self.speeds)):
            self.speeds[point].x *= 2
            self.speeds[point].y *= 2

    def decrease_speed(self):
        for point in range(len(self.speeds)):
            self.speeds[point].x /= 2
            self.speeds[point].y /= 2

    def add_multiple(self, num):
        for _ in range(num):
            self.add_point(Vec2d(random.random() * 800, random.random() * 600),
                           Vec2d(random.random() * 2, random.random() * 2))

            knot.add_point(Vec2d(random.random() * 800, random.random() * 600),
                           Vec2d(random.random() * 2, random.random() * 2))

    def remove_multiple(self, num):
        try:
            for _ in range(num):
                self.__delete__()
        except:
            return


class Knot(Polyline):
    def __init__(self, count):
        super().__init__()
        self.count = count

    def __delete__(self, num=None):
        if num is None:
            self.points.pop()
            self.speeds.pop()
        else:
            self.points.pop(num)
            self.speeds.pop(num)

    def add_point(self, point, speed):
        super().add_point(point, speed)
        self.get_knot()

    def delete_point(self, point=None):
        super().delete_point()
        self.get_knot()

    def set_points(self):
        super().set_points()
        self.get_knot()

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1

        if deg == 0:
            return points[0]

        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points):
        alpha = 1 / self.count
        res = []

        for i in range(self.count):
            res.append(self.get_point(base_points, i * alpha))

        return res

    def get_knot(self):
        if len(self.points) < 3:
            return []

        res = []

        for i in range(-2, len(self.points) - 2):
            points = [
                (self.points[i] + self.points[i + 1]) * 0.5, self.points[i + 1],
                (self.points[i + 1] + self.points[i + 2]) * 0.5
            ]

            res.extend(self.get_points(points))
        return res

    def draw_points(self, points, width=3, color=(255, 255, 255)):
        for p_n in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay,
                             color,
                             points[p_n].int_pair(),
                             points[p_n + 1].int_pair(),
                             width)


def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = [
        ["F1", "Show Help"],
        ["R", "Restart"],
        ["P", "Pause/Play"],
        ["Num+", "More points"],
        ["Num-", "Less points"],
        ["Arrow Up", "Increase speed"],
        ["Arrow Down", "Decrease speed"],
        ["A", "Add multiple points"],
        ["D", "Remove multiple points"],
        ["", ""],
        [str(len(polyline.points)), "Current points"]
    ]

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (300, 100 + 30 * i))


# Основная программа
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    multi = 3
    working = True
    polyline = Polyline()
    knot = Knot(steps)
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
                    polyline = Polyline()
                    knot = Knot(steps)
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                if event.key == pygame.K_UP:
                    polyline.increase_speed()
                if event.key == pygame.K_DOWN:
                    polyline.decrease_speed()
                if event.key == pygame.K_q:
                    polyline.add_multiple(multi)
                if event.key == pygame.K_a:
                    polyline.remove_multiple(multi)

            if event.type == pygame.MOUSEBUTTONDOWN:
                speed = Vec2d(random.random() * 2, random.random() * 2)
                polyline.add_point(Vec2d(event.pos), speed)
                knot.add_point(Vec2d(event.pos), speed)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        polyline.draw_points(polyline.points)
        knot.draw_points(knot.get_knot(), 3, color)

        if not pause:
            polyline.set_points()
            knot.set_points()

        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
