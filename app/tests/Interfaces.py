"""
Meta Class Module for test.
:mod: `Physical` 모듈
=============================================
..author : Kang Won Ji, Lee Geun Ha.

description
============
this module has
testable use objects instantiated from this class.
"""
class Testable(object):


    def RunTest(self):
        pass


class Resetable(Testable):

    def StartTest(self):
        pass

    def StopTest(self):
        pass


