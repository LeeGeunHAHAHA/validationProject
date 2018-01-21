from tests.Testable import *

class IORandom(Testable):
    lba=1024
    strtpos = 0

    def runTest(self):
        print("this is proto type from IOrandom")

if __name__ == "__main__":
    ior = IORandom()
    ior.runTest()
