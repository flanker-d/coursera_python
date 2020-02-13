from queue import Queue
from threading import Thread

def worker(q, n):
    while True:
        item = q.get()
        if item is None:
            break
        print("process data:", n, item)

q = Queue(5)

th1 = Thread(target=worker, args=(q, 1))
th2 = Thread(target=worker, args=(q, 2))
th1.start()
th2.start()

for i in range(50):
    print("put:", i)
    q.put(i) #если тут будет 5 элементов, то метод заблокирует выполнение потока и будет ждать пока не появися свободное место в очереди

q.put(None)
q.put(None)

th1.join()
th2.join()