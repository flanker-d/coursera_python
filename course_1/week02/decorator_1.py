import functools

def logger(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        result = func(*args, **kwargs)
        with open("log.txt", "w") as f:
            f.write(str(result))
        return result
    return wrapped

@logger
def summator(num_list):
    return sum(num_list)

print(summator([x + 1 for x in range(50)]))
print(summator.__name__)

with open("log.txt", "r") as f:
    print("log.txt: {}".format(f.read()))