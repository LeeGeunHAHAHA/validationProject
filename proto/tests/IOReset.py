from tests.Testable import Testable

class IOReset(Testable):
    lba=1024
    strtpos = 0

    def runTest(self):
        print("this is proto type from IOReset")
