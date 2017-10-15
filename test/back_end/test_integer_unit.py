import unittest

from procsim.back_end.integer_unit import IntegerUnit
from procsim.back_end.result import Result
from procsim.feedable import Feedable
from procsim.instructions import Add
from procsim.instructions import AddI
from procsim.register_file import RegisterFile

class TestIntegerUnit(unittest.TestCase):

    def setUp(self):
        init_values = {'r%d' % i: i for i in range(10)}
        self.reg_file = RegisterFile(10, init_values=init_values)
        self.wu_stub = WriteUnitStub()

    def test_integer_unit_correct_result(self):
        """Test correct Result computed by IntegerUnit and fed to WriteUnit."""
        add = Add('r1', 'r3', 'r5')
        add.DELAY = 1
        unit = IntegerUnit(self.reg_file, self.wu_stub)
        unit.feed(add)
        unit.tick()
        unit.tick()
        self.assertEqual(self.wu_stub.result, Result('r1', 8))

    def test_integer_unit_busy(self):
        """Test IntegerUnit busy method updates correctly after ticks."""
        add = Add('r0', 'r1', 'r6')
        add.DELAY = 5
        addi = AddI('r3', 'r5', 10)
        addi.DELAY = 10
        for ins in [add, addi]:
            unit = IntegerUnit(self.reg_file, self.wu_stub)
            self.assertFalse(unit.busy(),
                             'IntegerUnit busy after initialization')
            unit.feed(ins)
            self.assertTrue(unit.busy(),
                            'IntegerUnit not busy after being fed')
            for _ in range(ins.DELAY - 1):
                unit.tick()
                self.assertTrue(unit.busy(),
                                'IntegerUnit not busy before DELAY ticks')
            unit.tick()
            self.assertFalse(unit.busy(),
                             'IntegerUnit busy after DELAY ticks')

class WriteUnitStub(Feedable):
    """Stub to receive IntegerUnit Results from.

    Attributes:
        result: Result set on feed. (default None)
    """
    def __init__(self):
        self.result = None

    def feed(self, result):
        self.result = result

    def busy(self):
        return False
