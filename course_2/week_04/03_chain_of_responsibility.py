class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""

class EventGet:
    def __init__(self, type):
        self.type = type

class EventSet:
    def __init__(self, value):
        self.value = value

class NullHandler:
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, event):
        if self.__successor is not None:
            return self.__successor.handle(obj, event)

class IntHandler(NullHandler):
    def handle(self, obj, event):
        if isinstance(event, EventGet):
            if event.type == int:
                return obj.integer_field
            else:
                return super().handle(obj, event)
        elif isinstance(event, EventSet):
            if type(event.value) == int:
                obj.integer_field = event.value
            else:
                return super().handle(obj, event)

class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if isinstance(event, EventGet):
            if event.type == float:
                return obj.float_field
            else:
                return super().handle(obj, event)
        elif isinstance(event, EventSet):
            if type(event.value) == float:
                obj.float_field = event.value
            else:
                return super().handle(obj, event)

class StrHandler(NullHandler):
    def handle(self, obj, event):
        if isinstance(event, EventGet):
            if event.type == str:
                return obj.string_field
            else:
                return super().handle(obj, event)
        elif isinstance(event, EventSet):
            if type(event.value) == str:
                obj.string_field = event.value
            else:
                return super().handle(obj, event)

if __name__ == "__main__":
    obj = SomeObject()
    obj.integer_field = 42
    obj.float_field = 3.14
    obj.string_field = "some text"
    chain = IntHandler(FloatHandler(StrHandler(NullHandler)))

    int_val = chain.handle(obj, EventGet(int))
    assert int_val == 42

    float_val = chain.handle(obj, EventGet(float))
    assert float_val == 3.14

    str_val = chain.handle(obj, EventGet(str))
    assert str_val == 'some text'

    chain.handle(obj, EventSet(100))
    assert chain.handle(obj, EventGet(int)) == 100

    chain.handle(obj, EventSet(0.5))
    assert chain.handle(obj, EventGet(float)) == 0.5

    chain.handle(obj, EventSet('new text'))
    assert chain.handle(obj, EventGet(str)) == 'new text'