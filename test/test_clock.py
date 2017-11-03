import random
import unittest

from procsim.clock import Clock
from procsim.clocked import Clocked

class TestClock(unittest.TestCase):

    def setUp(self):
        self.clock = Clock()
        self.stubs = [ClockedStub(), ClockedStub()]
        for stub in self.stubs:
            self.clock.register(stub)

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

    def test_n_ticks(self):
        """Ensure Clock records number of tick calls."""
        exp_n_ticks = 0
        self.assertEqual(self.clock.n_ticks, exp_n_ticks,
                         'Clock n_ticks should be 0 after instantiation')

        for _ in range(100):
            more_ticks = random.randint(0, 100)
            for _ in range(more_ticks):
                self.clock.tick()
            exp_n_ticks += more_ticks
            self.assertEqual(self.clock.n_ticks, exp_n_ticks,
                             'Clock n_ticks should be %d, got %d' % (exp_n_ticks,
                                                                     self.clock.n_ticks))

class ClockedStub(Clocked):
    def __init__(self):
        self.operate_called = False
        self.trigger_called = False

    def operate(self):
        self.operate_called = True

    def trigger(self):
        self.trigger_called = True
