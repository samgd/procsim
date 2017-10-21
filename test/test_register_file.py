import unittest

from procsim.register import Register
from procsim.register_file import RegisterFile

class TestRegisterFile(unittest.TestCase):

    def test_eq(self):
        reg_file1 = RegisterFile(3, gpr_prefix='R', init_values={'R1': 10, 'R2': -1})
        reg_file2 = RegisterFile(3, gpr_prefix='R', init_values={'R1': 10, 'R2': -1})
        self.assertTrue(reg_file1 == reg_file2)
        reg_file2['R0'] += 1
        self.assertTrue(reg_file1 != reg_file2)

    def test_get(self):
        name = 'X3'
        exp = 10
        reg_file = RegisterFile(4, gpr_prefix='X', init_values={name: exp})
        got = reg_file[name]
        self.assertEqual(got, exp,
                         '%s returned %s, should be %s' % (name, got, exp))

    def test_set(self):
        reg_file = RegisterFile(5, gpr_prefix='Y')
        name = 'Y2'
        exp = -100
        reg_file[name] = exp
        got = reg_file[name]
        self.assertEqual(got, exp,
                         '%s returned %s, should be set to %s' % (name, got, exp))

    def test_len(self):
        n_gpr_registers = 10
        reg_file = RegisterFile(n_gpr_registers)
        act_len = len(reg_file)
        n_registers = n_gpr_registers + 1 # Count PC Register.
        self.assertEqual(act_len, n_registers,
                         'len should be %d not %s' % (n_registers, act_len))

    def test_repr(self):
        reg_file = RegisterFile(3, gpr_prefix='R', init_values={'R1': 10, 'R2': -1})
        self.assertEqual(reg_file, eval(repr(reg_file)))
