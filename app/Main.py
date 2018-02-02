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
def makeTestQueue(phyList,input_list, main_input):
    testFlag = main_input['Test']
    testQ = q()
    if testFlag == "IO":
        testQ = IOEach.makeIOTestQueue(phyList,input_list)
        return testQ 
    else :
        testQ = Resets.QueueParser(IOEach.makeIOTestQueue(phyList,input_list))
        return testQ



def parseInput():
    input_file = open("./configuration","r")
    lines = input_file.readlines()
    i = 0
    input0 = {}
    input1 = {}
    main_input = {}
    tmp_list = [main_input,input0, input1]

    for line in lines:
        tmp = list(line.split(" "))
        colonPos = line.find(":")
        if(colonPos == -1):
            i += 1
        else:
            tmp_list[i].setdefault(tmp[0], line[colonPos+2:-1])

    input0['target_namespace'] = list(map(lambda ns: "lun"+ns,input0['target_namespace'].split(" ")))  # lun list
    input1['target_namespace'] = list(map(lambda ns: "lun" + ns, input1['target_namespace'].split(" ")))  # lun list


    return main_input, input0, input1



if __name__ == "__main__":
    main_input, input0, input1 = parseInput()
    input_list = [input0, input1]
    phy1 = PhysicalFunction(input0)
    phy2 = PhysicalFunction(input1) if main_input['port'] == "dual" else None
    if main_input['port'] == "single": input1 = None
    phyList = [phy1, phy2] 
    try :
        phyList.remove(None)
        input_list.remove(None)
    except :
        pass
    test1 = makeTestQueue(phyList,input_list, main_input)
    testRunner = TestRunner.Runner(test1)
    singmul = main_input['Threads']
    if singmul == "multi":
        testRunner.TestInMultiThread()
    else :
        testRunner.TestInSequential()


