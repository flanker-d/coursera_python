class Polite:
    def __delattr__(self, item):
        value = getattr(self, item)
        print('Goodbuy {}, you were {}!'.format(item, value))

        object.__delattr__(self, item)

def _main():
    obj = Polite()
    obj.attr = 10
    del obj.attr

if __name__ == "__main__":
    _main()