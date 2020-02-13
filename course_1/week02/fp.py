#######
#caller
#######

def caller(func, params):
    return func(*params)

def printer(name, origin):
    print("key = {} : val = {}".format(name, origin))

caller(printer, ["zeba", "trading"])

#######
#closure
########

def get_multiplier():
    def inner(a, b):
        return a * b
    return inner

m = get_multiplier()
print(m(10, 11))

def get_multiplier(number):
    def inner(a):
        return a * number
    return inner

m_by_2 = get_multiplier(2)
print(m_by_2(10))

######
#map
######
def squarify(a):
    return a ** 2

print(list(map(squarify, range(5)))) # итерируется по range и применяет функцию squarify

# equiv map
squared_list = []
for number in range(5):
    squared_list.append(squarify(number))
print(squared_list)


#######
#filter
#######

def is_positive(a):
    return a > 0

print(list(filter(is_positive, range(-2, 3))))

# equiv filter

positive_list = []
for number in range(-2, 3):
    if is_positive(number):
        positive_list.append(number)
print(positive_list)

#######
#lambda
#######
print(list(map(lambda x: x ** 2, range(5))))
print(type(lambda x: x ** 2))
print(list(filter(lambda x: x > 0, range(-2, 3))))


#####
# ex1
#####
print(list(map(lambda x: str(x), range(-10, 10))))

#alt
def stringify_list(num_list):
    return list(map(str, num_list))
print(stringify_list(range(-10, 10)))

########
# functools
########

from functools import reduce

def mult(a, b):
    return a * b

print(reduce(mult, range(1, 6)))

from functools import partial

def greeter(person, greeting):
    return '{}, {}!'.format(greeting, person)

hier = partial(greeter, greeting='Hi')
helloer = partial(greeter, greeting='Hello')

print(hier('brother'))
print(helloer('sir'))


#######
# list_comperhensions
#######

square_list = [number ** 2 for number in range(10)]
print(square_list)

even_list = [num for num in range (10) if num % 2 == 0]
print(even_list)

square_map = {number: number ** 2 for number in range(5)}
print(square_map)

reminders_set = {num % 11 for num in range(100)}
print(reminders_set)

print(num % 11 for num in range(100))


#####
# zip
#####

num_list = range(7)
squared_list = [x ** 2 for x in num_list]
cubed_list = [x ** 3 for x in num_list]

print(list(zip(num_list, squared_list, cubed_list)))


#####
# ex2
#####
print(list(zip(filter(bool, range(3)), [x ** 2 for x in range(3) if x > 0])))
