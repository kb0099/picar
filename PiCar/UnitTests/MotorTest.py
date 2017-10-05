"""Unit tests for the Motor class

'mock' is available as of Python 3.3
"""
#import sys
#sys.path.insert(0,'..')

# Imports
import mock
import unittest
from .. import motor

class TestMotorClass(unittest.TestCase):
	
	def test_construct(self):
		"""Test constructor behaves as expected.
		"""
		# check frwd_p, bkwd_p, enbl_p
		
		# check GPIO.setup is called right
		
		# check GPIO.pwm is called right, returns a test dummy
		
		# check pwm

if __name__ == '__main__':
	unittest.main()