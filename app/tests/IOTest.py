#!/usr/bin/env python3
import sys
import os
from subprocess import call
sys.path.insert(0, os.path.abspath('../'))
from Functions import *
import random
class IOTest():
    """
    This class have information about I/O sequential/ I/O random test.
    When initiate this class, user can run test RunTest method.
    """
    target_function1 = None
    target_function2 = None
    numOfVF = None
    port = None
    port2 = None
    targetNum = None
    MAXLBA = 65536
    limit_size = None
    testType = ""   # read, write, compare
    testPattern = ""   # random, sequential
    targetNum_list= []

    def __init__(self, Physical_function1, Physical_function2):
        self.target_function1 = Physical_function1
        self.target_function2 = Physical_function2

        self.numOfVF = Physical_function1.numOfVF
        if Physical_function2 == None :  # single
            self.limit_size = 4096
        else :     # dual
            self.targetNum_list.append(self.target_function2.targetNum)
            self.numOfVF += Physical_function2.numOfVF
            self.limit_size = 2048
            self.port2 = Physical_function2.port

        self.targetNum_list.append(self.target_function1.targetNum)
        for i in range(int(self.numOfVF)):
            self.targetNum_list.append(i)

        self.port = Physical_function1.port


    def GetOption(self):
        '''
        To initailize member variable, this function requests information to user
        :param
        :return
        '''
        self.testType = input("testType ( Read | Write | Compare ) : ")
        self.testPattern = input("testPatter ( random | seq ) : ")


    def RunTest(self):
        '''
            This function runs a I/O test
            :param
        '''
        self.GetOption()
        if(self.testPattern == "random"):
            self.RandomTest()
        else:
            self.SeqTest()

    def SeqTest(self):
        '''
            This function starts a sequential test
            :param
        '''
        port_file = open("/iport0/port", 'w')
        for cnt in range(0,len(self.targetNum_list)):
            target = open("/iport0/target" + str(self.targetNum_list[cnt]), 'w')	
            port_file.write("Testlimits=" + str(self.limit_size) + "," + str(cnt * self.limit_size) + ",0 ")
            target.write("WriteEnabled=1 ")
            target.close()
            target = open("/iport0/target" + str(self.targetNum_list[cnt]), 'w')	
            target.write(self.testType+"_" + str(self.targetNum_list[cnt]) + ",1,1,0,1,0,0,0,-1,60,0,1,1,0,1:1,1:1,0,-0 ")


    def RandomTest(self):
        '''
            This function starts a random test
            :param
        '''

        randomSize = 0
        total = 0
        end_cnt = 0
        sizeArr = []
        for cnt in range(len(self.targetNum_list), 0, -1):
            tmp = self.MAXLBA / cnt
            randomSize = random.randint(int(tmp * 0.8), int(tmp * 1.3))
            self.MAXLBA -= randomSize
            total += randomSize
            sizeArr.append(randomSize)


        port_file = open("/iport0/port", 'w')
        for cnt in range(0,len(self.targetNum_list)):
            target = open("/iport0/target" + str(self.targetNum_list[cnt]), 'w')
            port_file.write("Testlimits=" + str(sizeArr[cnt]) + "," + str(sum(sizeArr[:cnt])) + ",0 ")
            target.write("WriteEnabled=1 ")
            target.close()
            target = open("/iport0/target" + str(self.targetNum_list[cnt]), 'w')
            target.write(self.testType+"_" + str(self.targetNum_list[cnt]) + ",1,1,0,1,0,0,0,-1,60,0,1,1,0,1:1,1:1,0,-0 ")


    def StopTest(self):
        '''
            This function stops all tests
            :param
        '''
        for cnt in range(0,len(self.targetNum_list)):
            targetN_file = open("/iport0/target/"+str(self.targetNum_list[cnt]))
            targetN_file.write("StopTests ")
        return 0

