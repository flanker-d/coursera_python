import os
from multiprocessing import Process

def f(name):
    print("pid: {} | hello, {}".format(os.getpid(), name))

p = Process(target=f, args=("Bob",))
p.start()
print("pid: {} | hello, {}".format(os.getpid(), "Bobik"))
p.join()