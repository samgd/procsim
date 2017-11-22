import unittest

from procsim.back_end.branch_unit import BranchUnit
from procsim.back_end.instructions.branch import Branch
from procsim.back_end.instructions.conditional import Conditional
from procsim.back_end.instructions.unconditional import Unconditional
from procsim.back_end.result import Result
from test.back_end.bus_log import BusLog

class TestBranchUnit(unittest.TestCase):

    def setUp(self):
        self.bus_log = BusLog()

    def test_correct_result(self):
        """Test correct Result computed by BranchUnit and published."""
        tests = []

        cond = Conditional('ROB1', lambda o1, o2: o1 < o2, 5, 6)
        cond.DELAY = 1
        tests.append((cond, Result('ROB1', True, typ=Branch)))

        cond = Conditional('ROB1', lambda o1, o2: o1 < o2, 6, 6)
        cond.DELAY = 1
        tests.append((cond, Result('ROB1', False, typ=Branch)))

        uncond = Unconditional('ROB2', 10)
        uncond.DELAY = 1
        tests.append((uncond, Result('ROB2', 10, typ=Branch)))

        for ins, exp_result in tests:
            self.bus_log.reset()
            unit = BranchUnit(self.bus_log)
            unit.feed(ins)
            unit.trigger()
            unit.tick()
            self.assertListEqual(self.bus_log.log, [exp_result])

    def test_full(self):
        """Test BranchUnit full method updates correctly after ticks."""
        cond = Conditional('ROB1', lambda o1, o2: o1 < o2, 11, 13)
        cond.DELAY = 5

        uncond = Unconditional('ROB1', 101)
        uncond.DELAY = 10

        for ins in [cond, uncond]:
            unit = BranchUnit(self.bus_log)
            self.assertFalse(unit.full(),
                             'BranchUnit should not be full after initialization')
            unit.feed(ins)
            self.assertTrue(unit.full(),
                            'BranchUnit should be full after being fed')
            unit.trigger()
            for _ in range(ins.DELAY - 1):
                unit.tick()
                self.assertTrue(unit.full(),
                                'BranchUnit should be full before DELAY ticks')
            unit.tick()
            self.assertFalse(unit.full(),
                             'BranchUnit should not be full after DELAY ticks')

    def test_capability(self):
        unit = BranchUnit(self.bus_log)
        self.assertEqual(unit.capability(), Branch)

    def test_flush(self):
        """Ensure flush flushes the BranchUnit."""
        unit = BranchUnit(self.bus_log)
        unit.feed(Unconditional('ROB1', 1001))
        self.assertTrue(unit.full(),
                        'BranchUnit should be full after being fed')
        unit.flush()
        self.assertFalse(unit.full(),
                        'BranchUnit should not be full after flush')
