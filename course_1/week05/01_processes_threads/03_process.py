# memory not share, copy on read, or copy on writee
import os

foo = "bar"

pid = os.fork()
if pid == 0:
    #child
    foo = "baz"
    print("child: ", foo)
else:
    #parent
    print("parent: ", foo)
    os.wait()

# ps axf | grep 02_process.py