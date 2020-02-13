import threading

a = threading.RLock() #recursive lock
b = threading.RLock()

def foo():
    try:
        a.acquire()
        b.acquire()
    finally:
        # wrong release sequence
        a.release()
        b.release()

#deadlock - if run in over 9000 threads