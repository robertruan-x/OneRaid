
import unittest

from ..errors import OneRaidCommandGetVdlistError
import sys
sys.path.insert(0,"C:\\Users\\robert\\OneDrive\\Repos\\TEST\\OneRaid")

class TestStringMethods(unittest.TestCase):

    def test_OneRaidCommandCreateRaidError(self):
        try:
            raise OneRaidCommandGetVdlistError("eee", "perccli64")
        except Exception as e:
            print(e)

if __name__ == '__main__':
    unittest.main()
