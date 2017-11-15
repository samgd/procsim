import unittest

from procsim.back_end.instructions.load import Load
from procsim.back_end.instructions.store import Store
from procsim.back_end.result import Result

class TestLoadStore(unittest.TestCase):

    def test_receive_and_can_dispatch(self):
        for op in [Load, Store]:
            ins = op('ROB1', 'ROB2', 'ROB3')
            self.assertFalse(ins.can_dispatch())

            ins.receive(Result('ROB4', 0))
            self.assertFalse(ins.can_dispatch())

            ins.receive(Result('ROB1', 0))
            self.assertFalse(ins.can_dispatch())

            ins.receive(Result('ROB2', 7))
            self.assertEqual(ins.address, 7)
            self.assertTrue(ins.can_dispatch())

            ins.receive(Result('ROB3', 0))
            self.assertEqual(ins.value, 0)
            self.assertTrue(ins.can_dispatch())
