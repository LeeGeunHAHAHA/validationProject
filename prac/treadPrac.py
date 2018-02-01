import threading, time
from queue import Queue
import random
sa = 0
class a(threading.Thread):
    A = int()


    def test(self):
        time.sleep(random.randint(0,3))
        print( self.name)



q=Queue()
for i in range(10):
    q.put(a())

threads = []

objects= []

for i in range(10):
    x = q.get()
    th = threading.Thread(target=x.test, args=())
    objects.append(x)
    th.start()
    threads.append(th)

for i in threads:
    i.join()
for i in objects:
    print(i.name)

