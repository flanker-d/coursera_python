import pygame
import random
import math

SCREEN_DIM = (800, 600)

class Vec2d:
    """Class two-dimensional vectors"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)

    def __len__(self):  # length of two vectors
        return 2

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __mul__(self, other):
        """
        Multiplication of two vectors or multiplications of vectors and scalar
        :param other: vectors or scalar (int|float type)
        :return: Vec2d
        """
        if isinstance(other, Vec2d):
            return Vec2d(self.x * other.x, self.y * other.y)
        else:
            assert type(other) == int or type(other) == float, 'Wrong type of other param'
            return Vec2d(self.x * other, self.y * other)

    def int_pair(self):
        return int(self.x), int(self.y)


class Polyline:
    """Class draws lines and points"""

    def __init__(self):
        self.speeds = []
        self.points = []
        self.lines = []

    def add_point(self, vector):
        self.points.append(vector)
        self.speeds.append(Vec2d(random.random() * 2, random.random() * 2))
        self.lines = self.points

    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(self.lines) - 1):
                pygame.draw.line(gameDisplay, color, self.lines[p_n].int_pair(),
                                 self.lines[p_n + 1].int_pair(), width)

        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color,
                                    p.int_pair(), width)

    # Recalculation of control points coordinates
    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(- self.speeds[p].x, self.speeds[p].y)
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)



class Knot(Polyline):
    """ Class extends fields and methods of class Poliline
     and add some function to make curves by several count points """
    
    def __init__(self, count):
        super().__init__()
        self.count = count

    def __get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg]*alpha + self.__get_point(points, alpha, deg - 1)*(1 - alpha)

    def __get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.__get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            print('i=', i)
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
            res.extend(self.__get_points(ptn, self.count))

        return res

    def add_point(self, vector):
        super().add_point(vector)
        self.lines = self.get_knot()

    def set_points(self):
        super().set_points()
        self.lines = self.get_knot()


# Draw help window
def draw_help():
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


# Main program
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)
    knot = Knot(steps)

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
                    knot.count = steps
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                    knot.count = steps

            if event.type == pygame.MOUSEBUTTONDOWN:
                knot.add_point(Vec2d(*event.pos))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        knot.draw_points()
        knot.draw_points("line", 3, color)
        if not pause:
            knot.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)