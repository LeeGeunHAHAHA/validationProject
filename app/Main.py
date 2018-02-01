import os
import sys

sys.path.insert(0, os.path.abspath('./tests'))
sys.path.insert(0, os.path.abspath('./'))

from queue import Queue as q

import IOTest
import IOEach
import Resets
import TestRunner
from Functions import *

input_list = []
def makeTestQueue():
    IORQueue = q().queue
    for i in range(10):
        IORQueue.append(IOReset.IOReset())
        IORQueue.append(IORandom.IORandom())
        IORQueue.append(IOSeq.IOSeq())

    return IORQueue


def parseInput():
    input_file = open("./configuration","r")
    lines = input_file.readlines()
    i = 0
    for line in lines:
        colonPos = line.find(":")
        input_list.append(line[colonPos+2:-1])
    input_list[7] = list(map(lambda ns: "lun"+ns,input_list[7].split(" ")) )  # lun list
    print(input_list)
    return input_list

if __name__ == "__main__":
    input_list = parseInput()
    phy1 = PhysicalFunction(input_list)
    test0 = IOTest.IOTest(phy1, None)
    test1 = IOEach.makeIOTestQueue([phy1],input_list)
    ResetQueue = Resets.QueueParser(test1)
    testRunner = TestRunner.Runner(ResetQueue)
    testRunner.TestInMultiThread()
    #testRunner.TestInSequential(ResetQueue)
    #test0.RunTest()



