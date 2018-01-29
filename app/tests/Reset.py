"""
This module has Classes of Reset. Reset has child classes.
"""
from .Interfaces import *
from ..Functions import *

class Reset():
    '''
    This class is parent class of child classes.
    '''

    targetIO = list()
    phyFunc = PhysicalFunction()
    def __init__(self, functionList):
        self.targetIO = Resetable(functionList)

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
        return 0

    def getResults(self):
        ''''
        This function gets results
        :return:
        '''
        return 0

    def doAction(self):
        '''
        This function starts the reset test
        :return:
        '''
        return 0

    def getTimings(self):
        '''
        This function gets a actual time
        :return:
        '''
        return 0

    def quarchGlitch(self):
        ''''
        This function starts glitch
        :return:
        '''
        return 0

    def stopIO(self):
        '''
        This function stops all reset tests
        :return:
        '''
        return 0

class SubsystemReset(Reset):
    '''
    This class reset function on Subsystem level.
    '''
    def runTest(self):
        return 0



    def doAction(self):
        """
        This function request SANBlaze to reset on Subsystem level
        """
        return 0

class FLR(Reset):
    '''
    This class reset function on FLR level.
    '''
    def runTest(self):
        return 0



    def doAction(self):
        """
        This function request SANBlaze to reset on FLR level
        """
        return 0

class ControllerReset(Reset):
    '''
    This class reset function on Contrller level.
    '''
    def runTest(self):
        return 0



    def doAction(self):
        """
        This function request SANBlaze to reset on Controller level
        """
        return 0

class PERST(Reset):
    '''
    This class reset function on PERST level.
    '''
    def runTest(self):
        return 0


    def doAction(self):
        """
        This function request SANBlaze to reset on PERST level
        """
        return 0
