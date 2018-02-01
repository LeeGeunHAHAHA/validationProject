from queue import Queue as q
import threading

class Runner():

    testQ = q()
    threads = []

    def __init__(self, tQ):
        self.testQ= tQ

    def TestInMultiThread(self):
        for i in range(self.testQ.qsize()):
            f = self.testQ.get()
            th = threading.Thread(target=f.RunTest, args=())
            th.start()
            self.threads.append(th)

        for th in self.threads:
            th.join()
        print("end test in multi thread")

    def TestInSequential(self):
        for i in range(self.testQ.qsize()):
            self.testQ.get().RunTest()
        print("end test in sequential")
