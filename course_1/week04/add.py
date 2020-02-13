import random

class NoisyInt:

    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        noise = random.uniform(-1, 1)
        return self.value + other.value + noise

a = NoisyInt(10)
b = NoisyInt(20)

print(a + b)
print(a + b)
print(a + b)