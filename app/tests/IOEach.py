#!/usr/bin/env python3
import os
import sys
import random
sys.path.insert(0, os.path.abspath('../'))
from queue import Queue as q
from Functions import *

def testInNameSpace(functionList,input_list):
    testQueue  = q()

    total = 0
    sizeArr = []
    numOfFunc = 0
    testPos = 0
    MAXLBA = int(functionList[0].LBA)

    for PF in functionList:
        numOfFunc += (int(PF.numOfVF)+1)

    testLimitSize = int(MAXLBA) / numOfFunc
    sizeArr = [int(testLimitSize)]*numOfFunc
    print(testLimitSize)

    for phy in functionList:
        for lun in phy.lun_list:
            print("!!!!!!!!!!!!!!!!!!",lun.targetNum)
            testQueue.put(IOTest(lun, testPos,input_list))
            testPos += int(sizeArr.pop())
        for vf in phy.vfunction_list:
            for vlun in vf.lun_list:
                print("!!!!!!!!!!!!!!!!!!",vlun.targetNum)
                testQueue.put(IOTest(vlun, testPos,input_list))
                print("start position : "+str(testPos))
                testPos += int(sizeArr.pop())
            
    return testQueue

def makeIOTestQueue(functionList,input_list):
    testQueue  = q()

    total = 0
    sizeArr = []
    numOfFunc = 0
    testPos = 0
    MAXLBA = int(functionList[0].LBA)

    if input("insert y if want to IO test in name space level : ")== "y":
        return testInNameSpace(functionList, input_list)
    for PF in functionList:
        numOfFunc += (int(PF.numOfVF)+1)

    if input_list[8] == "y":
        for cnt in range(numOfFunc, 0, -1):
            tmp = MAXLBA / cnt
            randomSize = random.randint(int(tmp * 0.8), int(tmp * 1.3))
            MAXLBA -= randomSize
            total += randomSize
            sizeArr.append(randomSize)
    else:
        testLimitSize = int(MAXLBA) / numOfFunc
        sizeArr = [int(testLimitSize)]*numOfFunc
        print(testLimitSize)

    for phy in functionList:
        print("start position : "+str(testPos))
        testQueue.put(IOTest(phy, testPos,input_list))
        testPos += sizeArr.pop()
        print(phy.lun_list[0].targetNum)
        for vf in phy.vfunction_list:
            testQueue.put(IOTest(vf, testPos,input_list))
            print("start position : "+str(testPos))
            testPos += int(sizeArr.pop())
            print(vf.lun_list[0].targetNum)
    return testQueue





class IOTest():
    """
    This class have information about I/O sequential/ I/O random test.
    When initiate this class, user can run test RunTest method.
    """
    port = None
    targetNum = None
    MAXLBA = 65536
    limit_size = None
    testType = ""   # read, write, compare
    port_file = None
    startPos =None
    idfunc = None
    numOfThreads = None
    numOfBlocks = None


   #nvme_file = open("./proc/vlun/nvme", 'w')
    def __init__(self, function, startPos,input_list):
        self.targetNum = function.targetNum
        self.limit_size = 2048
        self.port = function.port
        self.startPos = startPos
        self.idfunc = function
        self.testType, self.numOfThreads, self.numOfBlocks = input_list[9:]
      
        #self.testType = input("testType (read | write | compare) : ")
        #self.numOfThreads = input("#Threads : ")
        #self.numOfBlocks = input("#Blocks : ")    

    def RunTest(self):
        '''
            This function runs a I/O test
            :param
        '''
        self.StartTest()
    def StartTest(self):
        '''
            This function starts a sequential test
            :param
        '''
        port_file = open("/iport"+self.port+"/port", 'w')
        target = open("/iport0/target" + str(self.targetNum), 'w')
        port_file.write("Testlimits=" + str(self.limit_size) + "," + str(self.startPos) + ",0 \n")
        target.write("WriteEnabled=1 \n")
        target = open("/iport0/target" + str(self.targetNum), 'w')
        target.write(self.testType + str(self.targetNum) + ","+str(self.numOfThreads)+","+str(self.numOfBlocks)+",0,1,0,0,0,-1,60,0,1,1,0,1:1,1:1,0,-0 ")
    def StopTest(self):
        '''
            This function stops all tests
            :param
        '''
        targetN_file = open("/iport0/target"+str(self.targetNum),"w")
        targetN_file.write("StopTests ")
