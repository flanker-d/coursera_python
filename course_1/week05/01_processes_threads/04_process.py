# file descriptors: share, copy on read, or copy on writee
import os

f = open("../data.txt")
foo = f.readline()

pid = os.fork()
if pid == 0:
    #child
    foo = f.readline()
    print("child: ", foo)
else:
    #parent
    foo = f.readline()
    print("parent: ", foo)
    os.wait()

# ps axf | grep 02_process.py