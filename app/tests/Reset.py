"""
This module has Classes of Reset. Reset has child classes.
"""

class Reset(Testable)
	"""
	This class is parent class of child classes.
	"""



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




	def runTest():
		return 0



	def doAction():
		return 0
	
class FLR(Reset):




	def runTest():
		return 0



	def doAction():
		return 0
	
class ControllerReset(Reset):




	def runTest():
		return 0



	def doAction():
		return 0
	
class PERST(Reset):




	def runTest():
		return 0



	def doAction():
		return 0
