"""Unit tests for the Motor class

'mock' is available as of Python 3.3
"""
# modify system path to access modules above
import sys
sys.path.append(sys.path[0] + "\\..")

# Imports
import unittest
#from mock import patch, Mock
from motor import Motor

class TestMotorClass(unittest.TestCase):
	
	def testConstruct(self):
		"""Test constructor behaves as expected.
		"""

		m = Motor(1, 2, 3)
		# check frwd_p, bkwd_p, enbl_p
		self.assertEqual(m.frwd_p, 1)
		self.assertEqual(m.bkwd_p, 2)
		self.assertEqual(m.enbl_p, 3)
		# check GPIO.setup is called right
		
		# check GPIO.pwm is called right, returns a test dummy
		
		# check pwm


if __name__ == '__main__':
	unittest.main()
