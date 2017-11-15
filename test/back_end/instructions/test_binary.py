import unittest

from procsim.back_end.instructions.binary import Binary
from procsim.back_end.result import Result

class TestBinaryInstructions(unittest.TestCase):

    def test_receive_and_can_dispatch(self):
        ins = Binary('ROB1', lambda o1, o2: o1 + o2, 'ROB2', 'ROB3')
        self.assertFalse(ins.can_dispatch())

        ins.receive(Result('ROB4', 0))
        self.assertFalse(ins.can_dispatch())

        ins.receive(Result('ROB2', 5))
        self.assertFalse(ins.can_dispatch())

        ins.receive(Result('ROB1', 0))
        self.assertFalse(ins.can_dispatch())

        ins.receive(Result('ROB3', 7))
        self.assertTrue(ins.can_dispatch())

        ins.receive(Result('ROB0', 0))
        self.assertTrue(ins.can_dispatch())

    def test_execute(self):
        ins = Binary('ROB10', lambda o1, o2: o1 + o2, 'ROB3', 'ROB4')
        with self.assertRaises(ValueError):
            ins.execute()
        ins.receive(Result('ROB3', 5))
        ins.receive(Result('ROB4', 7))
        self.assertEqual(ins.execute(), Result('ROB10', 12))
