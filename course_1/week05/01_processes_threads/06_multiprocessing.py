import os
from multiprocessing import Process

class PrintProcess(Process):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self) -> None:
        print("child  pid: {} | hello, {}".format(os.getpid(), self.name))

p = PrintProcess("Bob")
p.start()
print("parent pid: {} | hello, {}".format(os.getpid(), "Bobik"))
p.join()