"""
This module has Classes of Reset. Reset has child classes.
"""

import time
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../'))

from queue import Queue as q

import Functions
import IOEach



def queueParser(IOTestQue):
	resetQueue = q()
	phyFuncs = dict()
	vFuncs = dict()
	for each_test in IOTestQue:
		if type(each_test.idfunc) == Functions.PhysicalFunction:
			phyFuncs.setdefault(each_test.targetNum,each_test)
		else :
			vFuncs.setdefault(each_test.targetNum,each_test)
	print(phyFuncs, vFuncs)
	for phy in phyFuncs :
		resetQueue.put(FLR(phyFuncs[phy]))
	for vir in vFuncs :
		resetQueue.put(FLR(vFuncs[vir]))

	return resetQueue



class Reset():
    '''
    This class is parent class of child classes.
    '''
    resetable = None

    def __init__(self):
        return 0

    def runTest(self):
        '''
        This function calls method to reset VF or PF
        :return:
        '''
        return 0

    def startIO(self):
        '''
        This function starts a I/O test
        :return:
        '''
        self.targetIO.runTest()
        return 0

    def pollForTestStatus(self):
        '''
        This function checks the status of test
        :return:
        '''
        testCheck = os.system("cat /iport" + port + "/tests/" + testType + "| grep -c Running")
        if (testCheck):
            return 1
        else:
            testCheck = os.system("cat /iport" + port + "/tests/" + testType + "| grep -c Failed")
            if (testCheck):
                return 0
        return -1

    def sb_print(self, String):
        print(String)

    def getResults(self):
        ''''
        This function gets results
        :return:
        '''
        dateString = time.localtime()
        self.sb_print(dateString + ": Test Results:\n")
        toPrint = os.popen("cat /iport" + port + "/tests/" + testType)
        self.sb_print(toPrint)
        dateString = time.localtime()
        self.sb_print(dateString + ": Error Counters\n")
        toPrint = os.popen("cat /iport" + port + "/target" + target + " | grep Errors")
        self.sb_print(toPrint)
        toPrint = os.popen("cat /port" + port + "/target" + target + " | grep -i count")
        self.sb_print(toPrint)

        return 0

    def doAction(self):
        '''
        This function starts the reset test
        :return:
        '''
        pass

    def getTimings(self):
        '''
        This function gets a actual time
        :return:
        '''
        return 0

    def stopIO(self):
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

        def runTest(self):
            self.IO.startTest()
            localtime = list(time.localtime())  # year, mon, mday, hour, min, sec, wday, yday, isdst
            log_file = open(
                "nvme_resets_log\_" + localtime[2] + "-" + localtime[1] + "-" + localtime[0] + "\_" + localtime[
                    3] + "\_" + localtime[4] + "\_" + localtime[5])
            outString = "nvme_reset_timing_flr"
            status = Reset.pollForTestStatus()
            if (status == 0):
                print("Test status is Failed !")
                Reset.getResults()
                return
            elif (status == -1):
                print("Test status is Passed. This is unexpected !")
                Reset.getResults()
                return
            else:
                print("Test is still running.")

            self.doAction()
            time.sleep(10)
            # Reset.getTimings()
            self.IO.stopTest()
            # Reset.getResults()

        def doAction(self):
            """
            This function request SANBlaze to reset on FLR level
            """
            targetNum = self.resetable.targetNum
            reset = open("/proc/vlun")
            reset.write("reset_pci_func=" + str(targetNum) + " ")

            return 0


