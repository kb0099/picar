"""Unit tests for the Powertrain Class
"""
# modify system path to access modules above
import sys
sys.path.append(sys.path[0] + "\\..")

# Imports
import unittest
from powertrain import Powertrain

class TestPowertrainClass(unittest.TestCase):

    def testConstructor(self):
        """Test constructor behaves as expected.
        """

        p = Powertrain(1, 2, 3, 4, 5, 6)
        # check left and right Motor's have expected values
        self.assertEqual(p.left.frwd_p, 1)
        self.assertEqual(p.left.bkwd_p, 2)
        self.assertEqual(p.left.enbl_p, 3)
        self.assertEqual(p.right.frwd_p, 4)
        self.assertEqual(p.right.bkwd_p, 5)
        self.assertEqual(p.right.enbl_p, 6)

if __name__ == '__main__':
    unittest.main()
