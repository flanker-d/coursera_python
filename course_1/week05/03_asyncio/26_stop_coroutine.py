def grep(pattern):
    print("start grep")
    try:
        while True:
            line = yield
            if pattern in line:
                print(line)
    except GeneratorExit:
        print("stop grep")

g = grep("python")
next(g) #g.send(None)
g.send(("golang is better?"))
g.close()

g1 = grep("python")
next(g1) #g.send(None)
g1.send(("golang is better?"))
g1.throw(RuntimeError, "something wrong")