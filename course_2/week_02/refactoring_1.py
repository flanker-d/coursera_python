import pygame
import random
import math


SCREEN_DIM = (800, 600)


# 2d vector class
class Vec2d:

    def __init__(self, first_point=(0, 0), second_point=(0, 0)):
        self.coordinates = self.int_pair(int(second_point[0]) - int(first_point[0]),
                                         int(second_point[1]) - int(first_point[1]))

    def get_coordinate(self, num):
        if num == 0:
            return self.coordinates[0]

        if num == 1:
            return self.coordinates[1]

    def __add__(self, other):
        return Vec2d(second_point=(self.coordinates[0] + other.coordinates[0],
                                   self.coordinates[1] + other.coordinates[1]))

    def __sub__(self, other):
        return Vec2d(second_point=(self.coordinates[0] - other.coordinates[0],
                                   self.coordinates[1] - other.coordinates[1]))

    def __mul__(self, other):
        if isinstance(other, Vec2d):
            return self.coordinates[0] * other.coordinates[0] + self.coordinates[1] * other.coordinates[1]
        else:
            return Vec2d(second_point=(self.coordinates[0] * other, self.coordinates[1] * other))

    def __len__(self):
        return math.sqrt(self.coordinates[0] * self.coordinates[0] + self.coordinates[1] * self.coordinates[1])

    @staticmethod
    def int_pair(first_int, second_int):
        tuple_of_int = (int(first_int), int(second_int))
        return tuple_of_int


# Closed twisted line class
class Polyline:

    def __init__(self):
        self.points = list()
        self.speeds = list()

    def add_point(self, point, speed_):
        self.points.append(Vec2d(second_point=point))
        self.speeds.append(Vec2d(second_point=speed_))

    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].get_coordinate(0) > SCREEN_DIM[0] or self.points[p].get_coordinate(0) < 0:
                self.speeds[p] = Vec2d(second_point=(- self.speeds[p].get_coordinate(0),
                                                     self.speeds[p].get_coordinate(1)))
            if self.points[p].get_coordinate(1) > SCREEN_DIM[1] or self.points[p].get_coordinate(1) < 0:
                self.speeds[p] = Vec2d(second_point=(self.speeds[p].get_coordinate(0),
                                                     - self.speeds[p].get_coordinate(1)))

    def draw_points(self, width=3, color_=(255, 255, 255)):
        for p in self.points:
            pygame.draw.circle(gameDisplay, color_, (p.get_coordinate(0), p.get_coordinate(1)), width)


# Closed twisted line class with calculation by added reference points
class Knot(Polyline):

    def __init__(self, steps_=1):
        super().__init__()
        self.steps = steps_
        self.knot_points = []

    def set_steps(self, steps_):
        self.steps = int(steps_) if int(steps_) > 0 else 1

    def get_steps(self):
        return self.steps

    def add_point(self, point, speed_):
        super().add_point(point, speed_)
        self.get_knot()

    def set_points(self):
        super().set_points()
        self.get_knot()

    def get_point(self, base_points, alpha, deg=None):
        if deg is None:
            deg = len(base_points) - 1
        if deg == 0:
            return base_points[0]
        return base_points[deg] * alpha + self.get_point(base_points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points_):
        alpha = 1 / self.steps
        res = list()
        for i in range(self.steps):
            res.append(self.get_point(base_points_, i * alpha))
        return res

    def get_knot(self):
        if len(self.points) < 3:
            return []
        self.knot_points = []
        for i in range(-2, len(self.points) - 2):
            ptn = list()
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            self.knot_points.extend(self.get_points(ptn))

    def draw_points(self, width=3, color_=(255, 255, 255)):
        for p_n in range(-1, len(self.knot_points) - 1):
            pygame.draw.line(gameDisplay, color_,
                             (self.knot_points[p_n].get_coordinate(0), self.knot_points[p_n].get_coordinate(1)),
                             (self.knot_points[p_n + 1].get_coordinate(0), self.knot_points[p_n + 1].get_coordinate(1)),
                             width)


# Drawing help
def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = list()
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([str(knot.get_steps()), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# Main program
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    working = True
    show_help = False
    pause = True
    polyline = Polyline()
    knot = Knot(35)

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
                    steps = knot.get_steps()
                    knot = Knot(steps)
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps = knot.get_steps()
                    knot.set_steps(steps + 1)
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps = knot.get_steps()
                    knot.set_steps(steps - 1)

            if event.type == pygame.MOUSEBUTTONDOWN:
                speed = (random.random() * 2, random.random() * 2)
                polyline.add_point(event.pos, speed)
                knot.add_point(event.pos, speed)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        polyline.draw_points()
        knot.draw_points(3, color)
        if not pause:
            polyline.set_points()
            knot.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
