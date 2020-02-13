#context manager
class suppress_exception:
    def __init__(self, exec_type):
        self.exec_type = exec_type

    def __enter__(self):
        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == self.exec_type:
            print('Nothing happend')
            return True #


with suppress_exception(ZeroDivisionError):
    really_big_number = 1 / 0


#import contextlib
#with contextlib.suppress(ValueError):
#   raise ValueError



