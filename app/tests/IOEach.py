#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.abspath('../'))
from queue import Queue as q
from Functions import *


def makeIOTestQueue(functionList):
    testQueue  = q().queue
    if input("type y if want to IO test in random : ") =="y":
        print("Not implemented yet")
    else :
        for phy in functionList:
            testPos = 0
            testLimitSize = functionList[0].LBA
            testQueue.append(IOTest(phy, 0))
            testPos += int(testLimitSize)
            for vf in phy.vfunction_list:
                testQueue.append(IOTest(vf, testPos))
                testPos += int(testLimitSize)
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
    #nvme_file = open("./proc/vlun/nvme", 'w')

    def __init__(self, function, startPos):
        self.targetNum = function.targetNum
        self.limit_size = 2048
        self.port = function.port
        self.startPos = startPos
        self.idfunc = function


    def GetOption(self):
        '''
        To initailize member variable, this function requests information to user
        :param
        :return
        '''
        self.testType = input("testType (read | write | compare) : ")

    def RunTest(self):
        '''
            This function runs a I/O test
            :param
        '''
        self.GetOption()
        self.startTest()

    def startTest(self):
        '''
            This function starts a sequential test
            :param
        '''
        port_file = open("/iport"+self.port+"/port", 'w')
        target = open("/iport0/target" + str(self.targetNum), 'w')
        port_file.write("Testlimits=" + str(self.limit_size) + "," + str(self.startPos) + ",0 \n")
        target.write("WriteEnabled=1 \n")
        target = open("/iport0/target" + str(self.targetNum), 'w')
        target.write(self.testType + str(self.targetNum) + ",1,1,0,1,0,0,0,-1,60,0,1,1,0,1:1,1:1,0,-0 ")

    def StopTest(self):
        '''
            This function stops all tests
            :param
        '''
        targetN_file = open("/iport0/target"+str(self.targetNum))
        targetN_file.write("StopTests")
