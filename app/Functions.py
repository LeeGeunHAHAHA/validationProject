"""
this module has information about PF, VF.
testable use objects instantiated from this class.
author : Kang Won Ji, Lee Geun Ha.
"""
class Function:
    port = None
    targetNum = None
    numOfQueue = None
    queueDepth = None
    LBA = 65536


class VirtualFunction(Function):
    """
    This class have information about virtual function.
    This class have numOfPhy, member variable that indicate parent physical function.
    """

    numOfPhy = None

    def __init__(self, parent):
        self.numOfPhy = parent



class PhysicalFunction(Function):
    """
    This class have information about physical function.
    If user wants to make virtual function, this class make virtual function.
    """
    numOfVF = None

    def vfEnable(self):
        """
        Instantiate as many as NumOfVF.
        :return: list that have instances of VF.
        """
        VFs=[VirtualFunction(self.targetNum) for i in range(self.numOfVF)]

        return VFs












    #def VF_Enable(target2, numvf,target1_file, target2_file):
    #    '''
    #        This function sets number of virtual functions
    #        :param:
#
    #    '''
    #    target1_file.write("NumVFs=" + numvf)
    #    if (target2 != ""):
    #        target2_file.write("NumVFs=" + numvf)
    #    return
#
#
    #def MakeQueue(target, target2, starttarget, endtarget2, endtarget, port, queuecnt, queuedepth, nvme_file):
    #    '''
    #        This function sets Queue Depth and num of Queue
    #        :param
    #    '''
    #    queuetarget = 0
    #    for looptarget in range(starttarget, endtarget2):
    #        # for VF
    #        if (looptarget <= endtarget):
    #            targetN_file = open("./iport" + port + "/target" + looptarget, 'w')
    #            targetN_file.write("QueueCount=" + queuecnt)
    #            targetN_file.write("QueueDepth=" + queuedepth)
    #            targetN_file.write("QueueAlignment=0")
    #            nvme_file.write("restart=" + looptarget)
    #        # for PF
    #        else:
    #            if (looptarget == endtarget + 1):
    #                queuetarget = target
    #            else:
    #                queuetarget = target2
    #            queuetarget_file = open("./iport" + port + "/target" + queuetarget, 'w')
    #            queuetarget_file.write("QueueCount=" + queuecnt)
    #            queuetarget_file.write("QueueDepth=" + queuedepth)
    #            queuetarget_file.write("QueueAlignment=0")
    #            nvme_file.write("restart=" + queuetarget)
    #    return
#


