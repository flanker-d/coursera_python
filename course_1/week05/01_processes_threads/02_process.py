import time
import os

pid = os.fork()
if pid == 0:
    #child
    while True:
        print("child: ", os.getpid())
        time.sleep(5)
else:
    #parent
    print("parent: ", os.getpid())
    os.wait()

# ps axf | grep 02_process.py