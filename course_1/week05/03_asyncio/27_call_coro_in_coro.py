def grep(pattern):
    print("start grep")
    while True:
        line = yield
        if pattern in line:
            print(line)

def grep_python_no_coro():
    g = grep("python")
    next(g)
    g.send("python is the best!")
    g.close()

def grep_pyhon_coro():
    g = grep("python")
    yield from g

g = grep_python_no_coro()

g1 = grep_pyhon_coro()
g1.send(None)
g1.send("python wow!")