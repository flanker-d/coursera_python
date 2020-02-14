class Light:
    def __init__(self, dim):
        """dim - кортеж из 2 чисел. Элемент dim[1] отвечает за высоту карты, dim[0] за ее ширину"""
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
        self.lights = []
        self.obstacles = []

    def set_dim(self, dim):
        """dim - кортеж из 2 чисел. Элемент dim[1] отвечает за высоту карты, dim[0] за ее ширину"""
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]

    def set_lights(self, lights):
        """устанавливает массив источников света с заданными координатами и просчитывает освещение"""
        self.lights = lights
        self.generate_lights()

    def set_obstacles(self, obstacles):
        """устанавливает массив препятствий с заданными координатами и просчитывает освещение"""
        self.obstacles = obstacles
        self.generate_lights()

    def generate_lights(self):
        return self.grid.copy()


class System:
    def __init__(self):
        """создается двухмерная, карта, на которой источники света обозначены как 1, а препятствия как -1."""
        self.map = self.grid = [[0 for i in range(30)] for _ in range(20)]
        self.map[5][7] = 1  # Источники света
        self.map[5][2] = -1  # Стены

    def get_lightening(self, light_mapper):
        """принимает в качестве аргумента объект, который должен посчитывать освещение.
        У объекта вызывается метод lighten, который принимает карту объектов и источников света и возвращает карту освещенности."""
        self.lightmap = light_mapper.lighten(self.map)


class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def lighten(self, grid):
        """принимает карту объектов и источников света и возвращает карту освещенности"""
        dim = (len(grid[0]), len(grid))  # Определение размера карты
        self.adaptee.set_dim(dim)
        lights = []
        obstacles = []
        for i in range(dim[0]):
            for j in range(dim[1]):
                if grid[j][i] == 1:
                    lights.append((i, j))
                elif grid[j][i] == -1:
                    obstacles.append((i, j))
        self.adaptee.set_lights(lights)
        self.adaptee.set_obstacles(obstacles)
        return self.adaptee.generate_lights()


if __name__ == "__main__":
    system = System()
    light = Light((10, 10))
    adapter = MappingAdapter(light)
    system.get_lightening(adapter)