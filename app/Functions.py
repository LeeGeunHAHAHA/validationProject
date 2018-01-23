"""
this module has information about PF, VF.
testable use objects instantiated from this class.
author : Kang Won Ji, Lee Geun Ha.
"""


class Function:
    """
    parent class of VF,PF
    """
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
        """
        constructor for initialize numOfPhy
        :param parent:
        """
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




