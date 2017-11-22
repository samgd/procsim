import unittest

from procsim.back_end.instructions.integer_logical import IntegerLogical
from procsim.back_end.integer_unit import IntegerUnit
from procsim.back_end.result import Result
from test.back_end.bus_log import BusLog

class TestIntegerUnit(unittest.TestCase):

    def setUp(self):
        self.bus_log = BusLog()

    def test_correct_result(self):
        """Test correct Result computed by IntegerUnit and published."""
        add = IntegerLogical('ROB1', lambda o1, o2: o1 + o2, 5, 6)
        add.DELAY = 1

        unit = IntegerUnit(self.bus_log)
        unit.feed(add)
        unit.trigger()
        unit.tick()
        self.assertEqual(self.bus_log.log, [Result('ROB1', 11)])

    def test_full(self):
        """Test IntegerUnit full method updates correctly after ticks."""
        add = IntegerLogical('ROB1', lambda o1, o2: o1 + o2, 11, 13)
        add.DELAY = 5
        sub = IntegerLogical('ROB1', lambda o1, o2: o1 - o2, 21, 7)
        sub.DELAY = 10
        for ins in [add, sub]:
            unit = IntegerUnit(self.bus_log)
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
        unit = IntegerUnit(self.bus_log)
        self.assertEqual(unit.capability(), IntegerLogical)

    def test_flush(self):
        """Ensure flush flushes the IntegerUnit."""
        unit = IntegerUnit(self.bus_log)
        unit.feed(IntegerLogical('ROB1', lambda o1, o2: o1 + o2, 11, 13))
        self.assertTrue(unit.full(),
                        'IntegerUnit should be full after being fed')
        unit.flush()
        self.assertFalse(unit.full(),
                        'IntegerUnit should not be full after flush')
