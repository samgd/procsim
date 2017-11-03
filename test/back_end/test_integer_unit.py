import unittest

from procsim.back_end.integer_unit import IntegerUnit
from procsim.back_end.result import Result
from procsim.feedable import Feedable
from procsim.instructions import Add
from procsim.instructions import AddI
from procsim.instructions import IntegerLogical
from procsim.register_file import RegisterFile
from test.feed_log import FeedLog

class TestIntegerUnit(unittest.TestCase):

    def setUp(self):
        init_values = {'r%d' % i: i for i in range(10)}
        self.reg_file = RegisterFile(10, init_values=init_values)
        self.feed_log = FeedLog()

    def test_correct_result(self):
        """Test correct Result computed by IntegerUnit and fed to WriteUnit."""
        add = Add('r1', 'r3', 'r5')
        add.DELAY = 1
        unit = IntegerUnit(self.reg_file, self.feed_log)
        unit.feed(add)
        unit.trigger()
        unit.tick()
        self.assertEqual(self.feed_log.log, [Result('r1', 8)])

    def test_full(self):
        """Test IntegerUnit full method updates correctly after ticks."""
        add = Add('r0', 'r1', 'r6')
        add.DELAY = 5
        addi = AddI('r3', 'r5', 10)
        addi.DELAY = 10
        for ins in [add, addi]:
            unit = IntegerUnit(self.reg_file, self.feed_log)
            self.assertFalse(unit.full(),
                             'IntegerUnit should not be full after initialization')
            unit.feed(ins)
            self.assertTrue(unit.full(),
                            'IntegerUnit should be full after being fed')
            unit.trigger()
            for _ in range(ins.DELAY - 1):
                unit.tick()
                self.assertTrue(unit.full(),
                                'IntegerUnit should be full before DELAY ticks')
            unit.tick()
            self.assertFalse(unit.full(),
                             'IntegerUnit should not be full after DELAY ticks')

    def test_capability(self):
        unit = IntegerUnit(self.reg_file, self.feed_log)
        self.assertEqual(unit.capability(), IntegerLogical)
