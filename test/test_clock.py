import unittest

from procsim.clock import Clock
from procsim.clocked import Clocked

class TestClock(unittest.TestCase):

    def setUp(self):
        self.clock = Clock()
        self.stubs = [ClockedStub(), ClockedStub()]
        for stub in self.stubs:
            self.clock.register(stub)

    def test_register_assertion(self):
        with self.assertRaises(AssertionError):
            self.clock.register('foo')

    def test_operate(self):
        self.clock.operate()
        for stub in self.stubs:
            self.assertTrue(stub.operate_called)
            self.assertFalse(stub.trigger_called)

    def test_trigger(self):
        self.clock.trigger()
        for stub in self.stubs:
            self.assertFalse(stub.operate_called)
            self.assertTrue(stub.trigger_called)

    def test_tick(self):
        self.clock.tick()
        for stub in self.stubs:
            self.assertTrue(stub.operate_called)
            self.assertTrue(stub.trigger_called)

class ClockedStub(Clocked):
    def __init__(self):
        self.operate_called = False
        self.trigger_called = False

    def operate(self):
        self.operate_called = True

    def trigger(self):
        self.trigger_called = True
