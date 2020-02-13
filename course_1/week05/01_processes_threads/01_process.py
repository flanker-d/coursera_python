import time
import os
pid = os.getpid()

while True:
    print(pid, time.time())
    time.sleep(2)

# ps aux | head -1; ps aux | grep 01_process.py
# strace -p <pid>
# lsof -p <pid>