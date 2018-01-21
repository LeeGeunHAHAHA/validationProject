from queue import Queue as q

class Runner:

    testQ = q()

    def __init__(self, tQ):
        self.testQ= tQ

    def run(self):
        while self.testQ:
            a = self.testQ.pop()
            a.runTest()
