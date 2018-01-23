#!/usr/bin/env python3
from random import *
class IOTest():

    def GetOption():
        '''
        To initailize member variable, this function requests information to user
        :param
        :return
        '''
        port =0  # tmp
        target = 1 # tmp
        target2 = 2  # tmp
        target1_file = open("./iport" + port + "/target" + target, 'w')
        target2_file = open("./iport" + port + "/target" + target2, 'w')
        nvme_file = open("./proc/vlun/nvme", 'w')
        numvf
        MAXLBA
        starttrget
        endtarget
        position
        endtarget2
        queuecnt
        queuedepth
        return 0


#    def ReadyReset():
#        '''
#        This function sets argument for reset
#        :param
#        :return
#        '''
#        return 0


    def RunTest(numvf, MAXLBA,starttarget, endtarget, position):
        '''
            This function runs a I/O test
            :param
        '''
        return 0


    def VF_Enable(target2, numvf,target1_file, target2_file):
        '''
            This function sets number of virtual functions
            :param:

        '''
        target1_file.write("NumVFs=" + numvf)
        if (target2 != ""):
            target2_file.write("NumVFs=" + numvf)
        return


    def MakeQueue(target, target2, starttarget, endtarget2, endtarget, port, queuecnt, queuedepth, nvme_file):
        '''
            This function sets Queue Depth and num of Queue
            :param
        '''
        queuetarget = 0
        for looptarget in range(starttarget, endtarget2):
            # for VF
            if (looptarget <= endtarget):
                targetN_file = open("./iport" + port + "/target" + looptarget, 'w')
                targetN_file.write("QueueCount=" + queuecnt)
                targetN_file.write("QueueDepth=" + queuedepth)
                targetN_file.write("QueueAlignment=0")
                nvme_file.write("restart=" + looptarget)
            # for PF
            else:
                if (looptarget == endtarget + 1):
                    queuetarget = target
                else:
                    queuetarget = target2
                queuetarget_file = open("./iport" + port + "/target" + queuetarget, 'w')
                queuetarget_file.write("QueueCount=" + queuecnt)
                queuetarget_file.write("QueueDepth=" + queuedepth)
                queuetarget_file.write("QueueAlignment=0")
                nvme_file.write("restart=" + queuetarget)
        return


    def SeqTest(numvf, MAXLBA,starttarget, endtarget, position):
        '''
            This function starts a sequential test
            :param
        '''
        return 0


    def RandomTest(numvf, MAXLBA,starttarget, endtarget, position):
        '''
            This function starts a random test
            :param
        '''
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



    if __name__ == "__main__":
        main()
