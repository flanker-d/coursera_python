import math

class Vec2d:
    """
    Двумерный вектор.

    Parameters
    ----------
    x: integer / float
        x-координата вектора.

    y: integet / float
        y-координата вектора.

    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vec2d({self.x}, {self.y})"

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vec2d(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vec2d(x, y)

    def __mul__(self, scalar):
        return Vec2d(self.x * scalar, self.y * scalar)

    def __len__(self):
        return 2

    def int_pair(self):
        return (self.x, self.y)