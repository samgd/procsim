import random
import unittest

import procsim.instructions as ins
from procsim.register_file import RegisterFile

class TestIntegerLogical(unittest.TestCase):

    def setUp(self):
        self.register_len = 10
        init_values = {'r%d' % i: i for i in range(self.register_len)}
        self.reg_file = RegisterFile(self.register_len,
                                     init_values=init_values)

    def test_add_execute(self):
        test_spec = {'op': ins.Add,
                     'exp_fn': lambda r1, r2: self.reg_file[r1] + self.reg_file[r2],
                     'arg_fn': lambda: (self.random_reg(),
                                        self.random_reg(),
                                        self.random_reg())}
        self.run_tests(test_spec)

    def test_addi_execute(self):
        test_spec = {'op': ins.AddI,
                     'exp_fn': lambda r1, v2: self.reg_file[r1] + v2,
                     'arg_fn': lambda: (self.random_reg(),
                                        self.random_reg(),
                                        random.randint(-10000, 10000))}
        self.run_tests(test_spec)

    def test_sub_execute(self):
        test_spec = {'op': ins.Sub,
                     'exp_fn': lambda r1, r2: self.reg_file[r1] - self.reg_file[r2],
                     'arg_fn': lambda: (self.random_reg(),
                                        self.random_reg(),
                                        self.random_reg())}
        self.run_tests(test_spec)

    def test_subi_execute(self):
        test_spec = {'op': ins.SubI,
                     'exp_fn': lambda r1, v2: self.reg_file[r1] - v2,
                     'arg_fn': lambda: (self.random_reg(),
                                        self.random_reg(),
                                        random.randint(-10000, 10000))}
        self.run_tests(test_spec)

    def test_mul_execute(self):
        test_spec = {'op': ins.Mul,
                     'exp_fn': lambda r1, r2: self.reg_file[r1] * self.reg_file[r2],
                     'arg_fn': lambda: (self.random_reg(),
                                        self.random_reg(),
                                        self.random_reg())}
        self.run_tests(test_spec)

    def test_muli_execute(self):
        test_spec = {'op': ins.MulI,
                     'exp_fn': lambda r1, v2: self.reg_file[r1] * v2,
                     'arg_fn': lambda: (self.random_reg(),
                                        self.random_reg(),
                                        random.randint(-10000, 10000))}
        self.run_tests(test_spec)

    # Test utilities.
    def run_tests(self, test_spec):
        """Run tests based on a test specification."""
        for i in range(100):
            (rd, r1, v2) = test_spec['arg_fn']()
            # Save rd value before execution to ensure it is not modified.
            rd_value = self.reg_file[rd]

            result = test_spec['op'](rd, r1, v2).execute(self.reg_file)

            self.assertEqual(self.reg_file[rd], rd_value,
                             'execute should not write to RegisterFile')
            self.assertEqual(result.dest, rd)
            self.assertEqual(result.value,
                             test_spec['exp_fn'](r1, v2))

    def random_reg(self):
        """Return a random but valid Register name."""
        return 'r%d' % random.randint(0, self.register_len - 2)
