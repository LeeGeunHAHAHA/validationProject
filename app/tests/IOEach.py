#!/usr/bin/env python3
import os
import sys
import random

sys.path.insert(0, os.path.abspath('../'))
from queue import Queue as q
from Functions import *


def testInNameSpace(functionList, input_list):
    '''

    **This function is blabla**


    :param functionList:
    :param input_list:
    :return: testQueue
    '''
    testQueue = q()

    total = 0

    sizeArr = []
    numOfFunc = 0
    testPos = 0
    MAXLBA = int(functionList[0].LBA)


    for PF in functionList:
        numOfFunc += (int(PF.numOfVF))

    testLimitSize = int(MAXLBA) / numOfFunc
    sizeArr = [int(testLimitSize)] * numOfFunc

    it = iter(input_list)
    for phy in functionList:
        input_dict = next(it)
       # for lun in phy.lun_list:
           # testQueue.put(IOTest(lun, testPos, input_dict))
        #    testPos += int(sizeArr[0])
        for vf in phy.vfunction_list:
            for vlun in vf.lun_list:
                testQueue.put(IOTest(vlun, testPos, input_dict))
                testPos += int(sizeArr.pop())
    return testQueue


def makeIOTestQueue(functionList, input_list):
    '''

    :param functionList:
    :param input_list:
    :return: testQueue
    '''
    testQueue = q()

    total = 0
    sizeArr = []
    numOfFunc = 0
    testPos = 0
    MAXLBA = int(functionList[0].LBA)

    it = iter(input_list)
    for phy in functionList:
        input_dict = next(it)
        if input_dict['is_namespaceLevel'] == "y":
            return testInNameSpace(functionList, input_list)
        for PF in functionList:
            numOfFunc += (int(PF.numOfVF) + 1)

        if input_dict['is_random'] == "y":
            for cnt in range(numOfFunc, 0, -1):
                tmp = MAXLBA / cnt
                randomSize = random.randint(int(tmp * 0.8), int(tmp * 1.3))
                MAXLBA -= randomSize
                total += randomSize
                sizeArr.append(randomSize)
        else:
            testLimitSize = int(MAXLBA) / numOfFunc
            sizeArr = [int(testLimitSize)] * numOfFunc
        testQueue.put(IOTest(phy, testPos, input_dict))
        testPos += sizeArr.pop()
        for vf in phy.vfunction_list:
            testQueue.put(IOTest(vf, testPos, input_dict))
            testPos += int(sizeArr.pop())
    return testQueue


class IOTest():
    """
    **This class have information about I/O sequential/ I/O random test.**
    **When initiate this class, user can run test RunTest method.**


    """
    port = None
    """
    This is port number for test.
    """
    targetNum = None
    """
    This is function number for test.
    """
    MAXLBA = 65536
    """
    This is maximum LBA size for test.
    """
    limit_size = None
    """
    This is limited LBA size for test.
    """
    testType = ""  # read, write, compare
    """
    This is testType. ( read | write | compare )
    """
    port_file = None
    """
    This is file 
    """
    startPos = None
    """
    This is test start position.
    """
    idfunc = None
    """
    This identifies function whether virtual function or physical function.
    """
    numOfThreads = None
    """
    This is number of threads for test.
    """
    numOfBlocks = None
    """
    This is number of blocks for test.
    """

    def __init__(self, function, startPos, input_dict):
        self.targetNum = function.targetNum
        self.limit_size = 512
        self.port = function.port
        self.startPos = startPos
        self.idfunc = function
        self.testType, self.numOfThreads, self.numOfBlocks = (input_dict['testType'], input_dict['#Threads'], input_dict['#Blocks'])

    def RunTest(self):
        '''
            This function runs a I/O test

        '''
        self.StartTest()
        
    def StartTest(self):
        '''
            This function starts a sequential test

        '''
        port_file = open("/iport" + self.port + "/port", 'w')
        target = open("/iport0/target" + str(self.targetNum), 'w')
        port_file.write("Testlimits=" + str(self.limit_size) + "," + str(self.startPos) + ",0 \n")
        target.write("WriteEnabled=1 \n")
        target = open("/iport0/target" + str(self.targetNum), 'w')
        target.write(self.testType + str(self.targetNum) + "," + str(self.numOfThreads) + "," + str(self.numOfBlocks) + ",0,1,0,0,0,-1,60,0,1,1,0,1:1,1:1,0,-0 ")

    def StopTest(self):
        '''
            This function stops all tests

        '''
        targetN_file = open("/iport0/target" + str(self.targetNum), "w")
        targetN_file.write("StopTests ")
