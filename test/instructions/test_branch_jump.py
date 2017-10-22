import random
import unittest

import procsim.instructions as ins
from procsim.register_file import RegisterFile
from procsim.back_end.result import Result

class TestBranchJump(unittest.TestCase):

    def setUp(self):
        self.register_len = 10
        init_values = {'r%d' % i: i for i in range(self.register_len)}
        self.reg_file = RegisterFile(self.register_len,
                                     init_values=init_values)

    def test_jump_execute(self):
        for _ in range(100):
            jump = ins.Jump(random.randint(0, 10000))
            result = jump.execute(self.reg_file)

            # Save PC value to ensure it remains unchanged.
            program_counter = self.reg_file['pc']

            self.assertEqual(result.dest, 'pc',
                             'execute Result dest should be pc')
            self.assertEqual(result.value, jump.imm,
                             'execute Result value should be imm')
            self.assertEqual(self.reg_file['pc'], program_counter,
                             'execute should not write to RegisterFile')
