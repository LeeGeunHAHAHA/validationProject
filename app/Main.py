from queue import Queue as q
from tests import *
import TestRunner


def makeTestQueue():
    IORQueue = q().queue
    for i in range(10):
        IORQueue.append(IOReset.IOReset())
        IORQueue.append(IORandom.IORandom())
        IORQueue.append(IOSeq.IOSeq())

    return IORQueue


if __name__ == "__main__":
    tq = makeTestQueue()
    testCase = testRunner.Runner(tq)
    testCase.run()



