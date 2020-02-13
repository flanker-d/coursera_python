from threading import Thread

class PrintThread(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print("th2 hello", self.name)

th = PrintThread("Bob")
th.start()
print("th1 hello", "Bobik")
th.join()