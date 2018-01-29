#!/usr/bin/env python3
from ..Functions import *
from .Interfaces import *
from .Reset import *


class IOTest(Testable, Resetable):
    """
    This class have information about I/O sequential/ I/O random test.
    When initiate this class, user can run test RunTest method.
    """
    target_function1 = None
    target_function2 = None
    numOfVF = None
    port = None
    targetNum = None
    LBA = None

    port_file = open("/iport0/port", 'w')
    nvme_file = open("./proc/vlun/nvme", 'w')

    def __init__(self,Physical_function1,Physical_function2):
        if Physical_function2 != None:
            self.target_function2 = Physical_function2
            port2, targetNum2, LBA2 = self.target_function2.setMember()
        self.target_function1 = Physical_function1
        port, targetNum, LBA = self.target_function1.setMember()

        self.numOfVF = Physical_function1.numOfVF
        if Physical_function2 == None :
            self.numOfVF += 0
        else :
            self.numOfVF += Physical_function2.numOfVF

        target1_file = open("./iport" + port + "/target" + targetNum, 'w')
        target2_file = open("./iport" + port2 + "/target" + targetNum2, 'w')



    def GetOption():
        '''
        To initailize member variable, this function requests information to user
        :param
        :return
        '''



    def RunTest(numvf, MAXLBA,starttarget, endtarget, position):
        '''
            This function runs a I/O test
            :param
        '''
        return 0


    def SeqTest(numvf, limit_size,start_target, end_target, position,method,port_file):
        '''
            This function starts a sequential test
            :param
        '''
        for target_cnt in range(start_target, end_target + 1):
            target = open("/iport0/target" + str(target_cnt), 'w')
            port_file.write("Testlimits=" + str(limit_size) + "," + str(target_cnt * limit_size) + ",0")
            target.write("WriteEnabled=1")
            target.write(method + str(target_cnt) + ",1,1,0,1,0,0,0,-1,60,0,1,1,0,1:1,1:1,0,-0")

        return 0


    def RandomTest(numvf, MAXLBA,start_target, end_target, position,port_file,method):
        '''
            This function starts a random test
            :param
        '''
        nsze = MAXLBA
        randomSize = 0
        total = 0
        end_cnt = 0
        sizeArr = []
        #        if (end_target == 29):
        #            end_cnt = 32  # dual
        #        else:
        #            end_cnt = 16  # single
        for target_cnt in range(end_cnt, 0, -1):
            tmp = nsze / target_cnt
            randomSize = randint(int(tmp * 0.8), int(tmp * 1.3))
            nsze -= randomSize
            total += randomSize
            sizeArr.append(randomSize)


        for target_cnt in range(start_target, end_target + 1):
            target = open("/iport0/target" + str(target_cnt), 'w')

            port_file.write("Testlimits=" + str(sizeArr[target_cnt]) + "," + str(sum(sizeArr[:target_cnt])) + ",0")
            target.write("WriteEnabled=1")
            target.write(method + str(target_cnt) + ",1,1,0,1,0,0,0,-1,60,0,1,1,0,1:1,1:1,0,-0")

        return 0


    def StopTest(starttarget, endtarget, target1_file, target, port):
        '''
            This function stops all tests
            :param
        '''
        for target in range(starttarget, endtarget+1):
            targetN_file = open("./iport"+port+"/target"+target)
            targetN_file.write("StopTests")
        return 0

    #if __name__ == "__main__":
    #main()
