#context manager
class open_file:

    def __init__(self, filename, mode):
        self.f = open(filename, mode)

    # для использования as
    def __enter__(self):
        return self.f

    # при выходе из контекстного менеджера
    def __exit__(self, *args):
        self.f.close()


with open_file('context_manager.log', 'w') as f:
    f.write('Inside `open_file` context manager')

with open_file('context_manager.log', 'r') as f:
    print(f.read())