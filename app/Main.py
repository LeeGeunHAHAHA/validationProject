import os
import sys

sys.path.insert(0, os.path.abspath('./tests'))
sys.path.insert(0, os.path.abspath('./'))
print(sys.path)

from queue import Queue as q
import IOTest
from Functions import *


def makeTestQueue():
    IORQueue = q().queue
    for i in range(10):
        IORQueue.append(IOReset.IOReset())
        IORQueue.append(IORandom.IORandom())
        IORQueue.append(IOSeq.IOSeq())

    return IORQueue



if __name__ == "__main__":
    phy1 = PhysicalFunction()
    test0 = IOTest.IOTest(phy1, None)
    test0.RunTest()



