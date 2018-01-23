"""
This module has Classes of Reset. Reset has child classes.
"""

class Reset():
    '''
    This class is parent class of child classes.
    '''


    def runTest():
        '''
        This function calls method to reset VF or PF
        :return:
        '''
        return 0

    def startTest():
        '''
        This function starts a I/O test
        :return:
        '''
        return 0

    def pollForTestStatus():
        '''
        This function checks the status of test
        :return:
        '''
        return 0

    def getResults():
        ''''
        This function gets results
        :return:
        '''
        return 0

    def doAction():
        '''
        This function starts the reset test
        :return:
        '''
        return 0

    def getTimings():
        '''
        This function gets a actual time
        :return:
        '''
        return 0

    def quarchGlitch():
        ''''
        This function starts glitch
        :return:
        '''
        return 0

    def stopTest():
        '''
        This function stops all reset tests
        :return:
        '''
        return 0

class SubsystemReset(Reset):
    '''
    This class reset function on Subsystem level.
    '''
    def runTest():
        return 0



    def doAction():
        """
        This function request SANBlaze to reset on Subsystem level
        """
        return 0

class FLR(Reset):
    '''
    This class reset function on FLR level.
    '''
    def runTest():
        return 0



    def doAction():
        """
        This function request SANBlaze to reset on FLR level
        """
        return 0

class ControllerReset(Reset):
    '''
    This class reset function on Contrller level.
    '''
    def runTest():
        return 0



    def doAction():
        """
        This function request SANBlaze to reset on Controller level
        """
        return 0

class PERST(Reset):
    '''
    This class reset function on PERST level.
    '''
    def runTest():
        return 0


    def doAction():
        """
        This function request SANBlaze to reset on PERST level
        """
        return 0
