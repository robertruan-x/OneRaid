

import unittest

from ..errors import OneRaidCommandGetVdlistError


class TestStringMethods(unittest.TestCase):

    def test_OneRaidCommandCreateRaidError(self):
        try:
            raise OneRaidCommandGetVdlistError("eee", "perccli64")
        except Exception as e:
            print(e)

if __name__ == '__main__':
    unittest.main()