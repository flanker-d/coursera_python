####
# ex1
###

class Descriptor:
    def __get__(self, instance, owner): #non-data descr
        print('get')

    def __set__(self, instance, value): #data descr
        print('set')

    def __delete__(self, instance): #data descr
        print('delete')

class Class:
    attr = Descriptor() #переопределено поведение set, get, delete

instance = Class()

instance.attr
instance.attr = 10
del instance.attr

####
# ex2
###

class Value:
    def __init__(self):
        self.value = None

    @staticmethod
    def _prepare_value(value):
        return value * 10

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = self._prepare_value(value)

class Class1:
    attr = Value()

instance = Class1()
instance.attr = 10

print(instance.attr)