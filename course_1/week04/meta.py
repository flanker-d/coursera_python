class Class:
    pass

obj = Class()

print(type(obj))   # obj создаётся Class'ом
print(type(Class)) # Class создаётся type'ом
print(type(type))  # type создаётся type'ом - это рекурсивная тема, которая реализована в C

print(issubclass(Class, type)) # Class создаётся type'ом, но не наследуется от него
print(issubclass(Class, object)) # Class наследуется от object'а

print('-----------------')

# create suimple class
def dummy_factory():
    class Class:
        pass

    return Class

Dummy = dummy_factory()

print(Dummy() is Dummy())

print('-----------------')

# how to python creates classes

NewClass = type('NewClass', (), {}) # так можно создать "на лету" класс

print(NewClass)
print(NewClass())

#но класс создаётся по-другому

print('-----------------')

class Meta(type):
    def __new__(cls, name, parents, attrs):
        print('Creating {}'.format(name))

        if 'class_id' not in attrs:
            attrs['class_id'] = name.lower()

        return super().__new__(cls, name, parents, attrs)


class A(metaclass=Meta):
    pass

print('A.class_id: {}'.format(A.class_id))


print('-----------------')

# логирует все созданные подклассы
class Meta1(type):
    def __init__(cls, name, bases, attrs):
        print('Initializing - {}'.format(name))

        if not hasattr(cls, 'registry'):
            cls.registry = {}
        else:
            cls.registry[name.lower()] = cls

        super().__init__(name, bases, attrs)

class Base(metaclass=Meta1):
    pass

class A1(Base):
    pass

class B1(Base):
    pass

print(Base.registry)
print(Base.__subclasses__())


# abstract methods (c++-way)
from abc import ABCMeta, abstractmethod

class Sender(metaclass=ABCMeta):
    @abstractmethod
    def send(self):
        """Do something"""

class Child(Sender):
    pass
    #def send(self): print('Sending')

Child()


#python way
class PythonWay:
    def send(self):
        raise NotImplementedError