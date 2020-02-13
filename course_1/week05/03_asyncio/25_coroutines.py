def grep(pattern):
    print("start grep")
    while True:
        line, val = yield
        if pattern in line:
            print(line)

g = grep("python")
next(g) #g.send(None)
g.send(("golang is better?", 1))
g.send(("python is simple", 2))