class Class:
    def method(self):
        pass

obj = Class()

print(obj.method)   # возвращается bound-метод
print(Class.method) # возвращается unbound-метод

class User:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

amy = User('Amy', 'Jones')

print(amy.full_name)  # вызывается функция
print(User.full_name) # вызывается property

#property - реализуется через дескрипторы

class Property:
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        if obj is None:
            return self
        return self.getter(obj)

class Class:
    @property
    def original(self):
        return 'original'

    @Property
    def custom_sugar(self):
        return 'custom_sugar'

    def custom_pure(self):
        return 'custom_pure'

    custom_pure = Property(custom_pure)


obj = Class()
# все 3 работают идентично
print(obj.original)
print(obj.custom_sugar)
print(obj.custom_pure)


#####
# static method
#####

class StaticMethod:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner=None):
        return self.func

####
# class method
####

class ClassMethod:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if owner is None:
            owner = type(obj)

        def new_func(*args, **kwargs):
            return self.func(owner, *args, **kwargs)

        return new_func

######
# slots
######

class Class:
    __slots__ = ['anakin'] # жестко заданный набор аттрибутов

    def __init__(self):
        self.anakin = 'the choosen one'

obj = Class()
obj.luke = 'the choosen two' # error