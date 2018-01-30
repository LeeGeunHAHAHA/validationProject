"""
:mod: `Physical` 모듈
=============================================
..author : Kang Won Ji, Lee Geun Ha.

description
============
this module has information about PF, VF.
testable use objects instantiated from this class.
"""

class Function:
    """
    - Function class
    ===================
    parent class of VF,PF. All Function class must implement this class.

    example :
     >>> class PhysicalFunction(Function)
     ...
    """
    port = None
    targetNum = None
    numOfQueue = None
    queueDepth = None
    LBA = 65536

    def __init__(self):
        """ constructor for Function class

        This Constructor get information by std.in (2018.01.21)
        default constructor to get information from user

        """
        self.port = input("insert target port to test : ")
        self.targetNum = input("insert target num : ")
        self.numOfQueue = input("insert number of queue : ")
        self.queueDepth = input("insert queue depth : ")
        self.LBA = input("insert max LBA size : ")
        self.makeQueue()


    def getMember(self):
        """
        To help other class initialize variations

        :return: return tuple of member variations
        example :
            >>> port, targetNum, numOfQueue, queueDepth, LBA = Function.getMember()

        """
        return self.port, self.targetNum, self.numOfQueue, self.queueDepth, self.LBA


    def makeQueue(self):
        """
        Make queue of functions.
        Number of Queue is member variation numOfQueue.
        Queue depth is member variation queueDepth.
        when function object is instantiated, this function is called from constructor.
        :return:
        example :
            >>> somefunction.makeQueue()
        """
        queue_target = open("/iport"+self.port+"/target"+self.targetNum, "w")
        queue_reset = open("/proc/vlun/nvme", "w")
        queue_target.write("QueueCount="+self.numOfQueue)
        queue_target.write("QueueDepth="+self.queueDepth)
        queue_target.write("QueueAlignment=0")
        queue_reset.write(self.targetNum)
        #do log echo



class VirtualFunction(Function):
    """
    * VirtualFunction class
    =========================
    This class have information about virtual function.
    This class have numOfPhy, member variable that indicate parent physical function.
    """

    numOfPhy = None

    def __init__(self, memTuple, target_number, parent):
        """
        constructor for initialize numOfPhy
        :param parent:
        example :
            >>> vf = VirtualFunction(101)
        """
        #super().__init__()
        self.port, self.targetNum, self.numOfQueue, self.queueDepth, self.LBA, self.numOfPhy = memTuple
        self.numOfPhy = parent
        self.targetNum = target_number


    def getMember(self):
        """
        To help other class initialize variations.
        In VirtualFunction, it returns mother Physical function

        :return: return tuple of member variations
        example :
            >>> port, targetNum, numOfQueue, queueDepth, LBA, numOfphy = somevf.getMember()
        """
        return self.port, self.targetNum, self.numOfQueue, self.queueDepth, self.LBA, self.numOfPhy


class PhysicalFunction(Function):
    """
    * PhysicalFunction class
    ===========================
    This class have information about physical function.
    If user wants to make virtual function, this class make virtual function.
    """
    numOfVF = None
    vfunction_list = list()

    def __init__(self):
        super().__init__()
        self.numOfVF = int(input("insert number of VF : "))
        self.vfunction_list = self.vfEnable()


    def vfEnable(self):
        """ vfEnable method
        Instantiate as many as NumOfVF.
        :return: list that have instances of VF.
        example :
            >>>vflist = somePF.vfEnable()
        """
        # do log echo
        vf = open("/iport"+self.port+"/target"+self.targetNum, "w")
        if self.numOfVF:
            idx = int(input("insert target num of starting VF function"))
            vf.write("NumVFs="+str(self.numOfVF))
            for idx in range(idx+self.numOfVF):
                self.vfunction_list.append(VirtualFunction(self.getMember(), idx, self.targetNum))
        return self.vfunction_list




    def getMember(self):
        """
        To help other class initialize variations.
        In PhysicalFunction, it returns vfuncrion list

        :return: return tuple of member variations
        example :
            >>> port, targetNum, numOfQueue, queueDepth, LBA, vfunction_list = somepf.getMember()
        """
        return self.port, self.targetNum,  self.numOfQueue, self.queueDepth, self.LBA, self.vfunction_list




if __name__ == "__main__":

    a = Function()
    b = PhysicalFunction()

    print(a.setMember())
    print(b.setMember())

