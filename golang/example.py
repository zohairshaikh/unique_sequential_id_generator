from ctypes import *
from Queue import Queue
from threading import Thread
lib = cdll.LoadLibrary("./generator.so")

def do_work():
    lib.run()

def worker():
    while True:
        print q.get()
        do_work()
        q.task_done()

q = Queue()
for i in range(50):
     t = Thread(target=worker)
     t.daemon = True
     t.start()

for i in range(50):
    q.put(i)

q.join()
