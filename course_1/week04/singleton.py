class Singleton:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

def _main():
    a = Singleton()
    b = Singleton()

    print (a is b)
    
if __name__ == "__main__":
    _main()