class Researcher:
    # вызывается когда аттрибут не найден
    def __getattr__(self, item):
        return 'Nothing found :('

    #вызывается всегда
    def __getattribute__(self, item):
        print('Looking for {}'.format(item))
        return object.__getattribute__(self, item)

    def foo(self):
        return 'I\'m foo'

def _main():
    obj = Researcher()

    print(obj.attr)
    print(obj.method)
    print(obj.SDFSDFSDFF)
    print(obj.foo)


if __name__ == "__main__":
    _main()