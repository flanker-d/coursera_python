def even_range(start, end):
    current = start
    while current < end:
        yield current
        current += 2

for number in even_range(0, 10):
    print(number)
print("\n")

ranger = even_range(0, 4)

print(next(ranger))
print(next(ranger))
#print(next(ranger))

print("\n")

def list_generator(list_obj):
    for item in list_obj:
        yield item
        print("after yielding {}".format(item))


generator = list_generator([1, 2, 3])

print(next(generator))
print(next(generator))


def fibonacci(number):
    a = b = 1
    for _ in range(number):
        yield a
        a, b = b, a + b

print(list(fibonacci(10)))

print("\n")

def accumulator():
    total = 0
    while True:
        value = yield total
        print("Got: {}".format(value))

        if not value: break
        total += value

generator = accumulator()
print(next(generator))
print("Accumulated: {}".format(generator.send(1)))
print("Accumulated: {}".format(generator.send(1)))
print("Accumulated: {}".format(generator.send(1)))
#print(next(generator))

