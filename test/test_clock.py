import unittest

from procsim.clock import Clock

class TestClock(unittest.TestCase):

    def setUp(self):
        self.clock = Clock()

    def test_register(self):
        with self.assertRaises(AssertionError):
            self.clock.register('foo')
