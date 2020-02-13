import functools

def logger(filename):
    def decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(filename, "w") as f:
                f.write(str(result))
            return result
        return wrapped
    return decorator

@logger("new_log.txt")
def summator(num_list):
    return sum(num_list)

summator([x + 1 for x in range(10)])

with open("new_log.txt", "r") as f:
    print(f.read())

print(summator.__name__)