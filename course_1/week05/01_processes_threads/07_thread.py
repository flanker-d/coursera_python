from threading import Thread

def f(name):
    print("th2 hello", name)

th = Thread(target=f, args=("Bob",))
th.start()
print("th1 hello", "Bobik")
th.join()