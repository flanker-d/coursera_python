import pygame
import random
import math

SCREEN_DIM = (800, 600)

class Vec2d:
     def __init__(self, vec):
         self._vec = vec
     
     def get_x1(self):
         return self._vec[0]

     def get_x2(self):
         return self._vec[1]

     def __add__(self,y):
        return Vec2d((self._vec[0] + y.get_x1(), self._vec[1] + y.get_x2()))

     def __sub__(self,y):
        return Vec2d((self._vec[0] - y.get_x1(), self._vec[1] - y.get_x2()))

     def __mul__(self, k):  # умножение вектора на число
         return Vec2d((self._vec[0] * k, self._vec[1] * k))     

     def __len__(self):
        return math.sqrt(self._vec[0] * self._vec[0] + self._vec[1] * self._vec[1])
    
     def int_pair(self):
        return self._vec       
     
     def scal_mul(self, k):  # скалярное умножение векторов
         return Vec2d((self._vec[0] * k, self._vec[1] * k))     
     
     def vec(self, y):  # создание вектора по началу (x) и концу (y) направленного отрезка
         return Vec2d((y.get_x1() - self._vec[0], y.get_x2() - self._vec[1]))
    
class Polyline:      
    def __init__(self):
        self._points = []
        self._speeds = []

    def add_point(self, point, speed=None):
        self._points.append(point)
        if (speed is not None):
            self._speeds.append(speed)
    
    def get_point(self, alpha, deg=None):
        if deg is None:
            deg = len(self._points) - 1
        if deg == 0:
            return self._points[0]
        return self._points[deg] * alpha + self.get_point(alpha, deg - 1) * (1 - alpha)  
    
    def get_points(self, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(i * alpha))
        return res
    
    def set_points(self):
        for p in range(len(self._points)):
            self._points[p] = self._points[p] + self._speeds[p]
            if self._points[p].get_x1() > SCREEN_DIM[0] or self._points[p].get_x1() < 0:
                 self._speeds[p] = (-  self._speeds[p][0],  self._speeds[p][1])
            if self._points[p].get_x2() > SCREEN_DIM[1] or self._points[p].get_x2() < 0:
                 self._speeds[p] = (self._speeds[p][0], - self._speeds[p][1])  

  


class Knot(Polyline):
    def __init__(self, steps):
        self._steps = steps
        self._res = []
        super().__init__()

    def add_point(self, point, speed=None):
        super().add_point(point,speed)
        self.get_knot()       

    def set_points(self):
        super().set_points()
        self.get_knot()
       
    def get_knot(self):
        if len(self._points) < 3:
            return []
        self._res = []

        for i in range(-2, len(self._points) - 2):
            ptn = Polyline()
            ptn.add_point((self._points[i] + self._points[i + 1]) * 0.5)
            ptn.add_point(self._points[i + 1])
            ptn.add_point((self._points[i + 1] + self._points[i + 2]) * 0.5)
            self._res.extend(ptn.get_points(self._steps))

    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(self._res) - 1):
                pygame.draw.line(gameDisplay, color, (int(self._res[p_n].get_x1()), int(self._res[p_n].get_x2())),
                                 (int(self._res[p_n + 1].get_x1()), int(self._res[p_n + 1].get_x2())), width)
    
        elif style == "points":
            for p in self._points:
                pygame.draw.circle(gameDisplay, color,
                                   (int(p.get_x1()), int(p.get_x2())), width)



# Отрисовка справки
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

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [(0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(text[1], True, (128, 128, 255)), (200, 100 + 30 * i))




# Основная программа
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")
  
    steps = 35
    working = True
    points = Knot(steps)  
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
                    points = Knot()                  
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                points.add_point(Vec2d(event.pos),(random.random() * 2, random.random() * 2))          

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        points.draw_points()        
        points.draw_points("line", 3, color)
        if not pause:
            points.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
