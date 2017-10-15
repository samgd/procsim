import unittest

from procsim.register import Register
from procsim.register_file import RegisterFile

class TestRegisterFile(unittest.TestCase):

    def test_eq(self):
        reg_file1 = RegisterFile(3, prefix='R', init_values={'R1': 10, 'R2': -1})
        reg_file2 = RegisterFile(3, prefix='R', init_values={'R1': 10, 'R2': -1})
        self.assertTrue(reg_file1 == reg_file2)
        reg_file2['R0'] += 1
        self.assertTrue(reg_file1 != reg_file2)

    def test_get(self):
        name = 'X3'
        exp = 10
        reg_file = RegisterFile(4, prefix='X', init_values={name: exp})
        got = reg_file[name]
        self.assertEqual(got, exp,
                         '%s returned %s, should be %s' % (name, got, exp))

    def test_set(self):
        reg_file = RegisterFile(5, prefix='Y')
        name = 'Y2'
        exp = -100
        reg_file[name] = exp
        got = reg_file[name]
        self.assertEqual(got, exp,
                         '%s returned %s, should be set to %s' % (name, got, exp))

    def test_len(self):
        n_registers = 10
        reg_file = RegisterFile(n_registers)
        act_len = len(reg_file)
        self.assertEqual(act_len, n_registers,
                         'len should be %d not %s' % (n_registers, act_len))

    def test_repr(self):
        reg_file = RegisterFile(3, prefix='R', init_values={'R1': 10, 'R2': -1})
        self.assertEqual(reg_file, eval(repr(reg_file)))
