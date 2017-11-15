import unittest

from procsim.back_end.instructions.unconditional import Unconditional
from procsim.back_end.result import Result

class TestUnconditional(unittest.TestCase):

    def test_receive_and_can_dispatch(self):
        ins = Unconditional('ROB1', 'ROB2')
        self.assertFalse(ins.can_dispatch())

        ins.receive(Result('ROB4', 0))
        self.assertFalse(ins.can_dispatch())

        ins.receive(Result('ROB2', 5))
        self.assertTrue(ins.can_dispatch())

        ins.receive(Result('ROB3', 0))
        self.assertTrue(ins.can_dispatch())

    def test_execute(self):
        ins = Unconditional('ROB10', 'ROB4')
        with self.assertRaises(ValueError):
            ins.execute()
        ins.receive(Result('ROB4', 7))
        self.assertEqual(ins.execute(), Result('ROB10', 7))
