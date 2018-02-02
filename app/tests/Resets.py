"""
This module has Classes of Reset. Reset has child classes.
"""

import time
import os
import sys
import copy
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../'))

from queue import Queue as q

import Functions
import IOEach



def QueueParser(IOTestQue):
	resetQueue = q()
	phyFuncs = dict()
	vFuncs = dict()
	qsze=IOTestQue.qsize()
	for each_test in range(qsze):
		target = IOTestQue.get()
		if type(target.idfunc) == Functions.PhysicalFunction:
			phyFuncs.setdefault(target.targetNum,target)
		else :
			vFuncs.setdefault(target.targetNum,target)
	for phy in phyFuncs :
		resetQueue.put(FLR(phyFuncs[phy]))
	for vir in vFuncs :
		resetQueue.put(FLR(vFuncs[vir]))

	return resetQueue



class Reset():
    '''
    This class is parent class of child classes.
    '''
    IO = None
    

    def __init__(self,IO):
        self.IO = IO  

    def RunTest(self):
        '''
        This function calls method to reset VF or PF
        :return:
        '''
        return 0

    def StartIO(self):
        '''
        This function starts a I/O test
        :return:
        '''
        self.targetIO.RunTest()
        return 0

    def PollForTestStatus(self,testName):
        '''
        This function checks the status of test
        :return:
        '''
        testCheck = os.popen("cat /iport" + str(self.IO.port) + "/tests/" + testName + "| grep -c Running")
        if (testCheck):
            return 1
        else:
            testCheck = os.popen("cat /iport" + str(self.IO.port) + "/tests/" + testName + "| grep -c Failed")
            if (testCheck):
                return 0
        return -1

    def sb_print(self, String):
        print(String)

    def GetResults(self,testName):
        ''''
        This function gets results
        :return:
        '''
        dateString = time.asctime()
        self.sb_print(dateString + ": Test Results:\n")
        toPrint = os.popen("cat /iport" + str(self.IO.port) + "/tests/" + testName)
        self.sb_print(toPrint.read())
        dateString = time.asctime()
        self.sb_print(dateString + ": Error Counters\n")
        toPrint = os.popen("cat /iport" + str(self.IO.port) + "/target" + str(self.IO.targetNum) + " | grep Errors")
        self.sb_print(toPrint.read())
        toPrint = os.popen("cat /iport" + str(self.IO.port) + "/target" + str(self.IO.targetNum) + " | grep -i count")
        self.sb_print(toPrint.read())

        return 0

    def DoAction(self):
        '''
        This function starts the reset test
        :return:
        '''
        pass

    def GetTimings(self):
        '''
        This function gets a actual time
        :return:
        '''
        return 0

    def StopTest(self):
        '''
        This function stops all reset tests
        :return:
        '''
        return 0

class FLR(Reset):
        '''
        This class reset function on FLR level.
        '''
        IO = None

        def __init__(self, IO):
            self.IO = IO

        def RunTest(self):
            testName = self.IO.testType + str(self.IO.targetNum)
            self.IO.StartTest()
           # localtime = list(time.localtime())  # year, mon, mday, hour, min, sec, wday, yday, isdst
           #log_file = open(
           #    "nvme_resets_log\_" + localtime[2] + "-" + localtime[1] + "-" + localtime[0] + "\_" + localtime[
           #        3] + "\_" + localtime[4] + "\_" + localtime[5])
            outString = "nvme_reset_timing_flr"
            status = self.PollForTestStatus(testName)
            if (status == 0):
                print("Test status is Failed !")
                self.GetResults(testName)
                return
            elif (status == -1):
                print("Test status is Passed. This is unexpected !")
                self.GetResults(testName)
                return
            else:
                print("Test is still running.")

            self.DoAction()
            time.sleep(10)
            # Reset.getTimings()
            self.IO.StopTest()
            # Reset.getResults()

        def DoAction(self):
            """
            This function request SANBlaze to reset on FLR level
            """
            targetNum = self.IO.targetNum
            reset = open("/proc/vlun/nvme","w")
            reset.write("reset_pci_func=" + str(targetNum) + " ")

            return 0


