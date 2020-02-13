class Logger:
    def __init__(self, filename):
        self.filename = filename

    def __call__(self, func):
        with open(self.filename, 'w') as f:
            f.write('Oh Danny boy...')
        return func

logger = Logger('call.txt')

#декорируемся объектом, а не классом
@logger
def completely_unless_function():
    pass

def _main():


    completely_unless_function()

    with open('call.txt') as f:
        print(f.read())

if __name__ == "__main__":
    _main()