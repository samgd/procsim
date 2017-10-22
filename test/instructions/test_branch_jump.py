import random
import unittest

from procsim.register_file import RegisterFile
import procsim.instructions as ins

class TestBranchJump(unittest.TestCase):

    def setUp(self):
        self.register_len = 10
        init_values = {'r%d' % i: i for i in range(self.register_len)}
        self.reg_file = RegisterFile(self.register_len,
                                     init_values=init_values)

    def test_jump_execute(self):
        """Ensure Jump execute returns correct Result."""
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

    def test_blth_execute(self):
        """Ensure Blth execute returns correct Result."""
        for _ in range(100):
            r1 = self.random_reg()
            r2 = self.random_reg()
            blth = ins.Blth(r1, r2, random.randint(0, 10000))

            # Save PC value to ensure it remains unchanged.
            program_counter = self.reg_file['pc']
            result = blth.execute(self.reg_file)
            self.assertEqual(self.reg_file['pc'], program_counter,
                             'execute should not write to RegisterFile')

            if r1 >= r2:
                self.assertIsNone(result)
                continue

            self.assertEqual(result.dest, 'pc',
                             'execute Result dest should be pc')
            self.assertEqual(result.value, blth.imm,
                             'execute Result value should be imm')

    def random_reg(self):
        """Return a random but valid Register name."""
        return 'r%d' % random.randint(0, self.register_len - 1)
