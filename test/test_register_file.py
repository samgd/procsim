import unittest

from procsim.register import Register
from procsim.register_file import RegisterFile

class TestRegisterFile(unittest.TestCase):

    def test_eq(self):
        reg_file1 = RegisterFile(3, prefix='R', init_values={'R1': 10, 'R2': -1})
        reg_file2 = RegisterFile(3, prefix='R', init_values={'R1': 10, 'R2': -1})
        self.assertTrue(reg_file1 == reg_file2)
        reg_file2['R0'] += 1
        self.assertTrue(reg_file1 == reg_file2,
                        'RegisterFiles should be equal after update but before tick')
        reg_file2.tick()
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
        self.assertEqual(reg_file[name], 0,
                        'value should not be set before tick')
        reg_file.tick()
        got = reg_file[name]
        self.assertEqual(got, exp,
                         '%s returned %s, should be set to %s' % (name, got, exp))

    def test_defensive_copy(self):
        """Ensure Registers cannot be written to outside of tick."""
        reg_file = RegisterFile(1, prefix='R', init_values={'R0': 10})
        reg = reg_file['R0']
        reg.write(99)
        self.assertEqual(reg_file['R0'], 10,
                         'Register update possible without tick')

    def test_len(self):
        n_registers = 10
        reg_file = RegisterFile(n_registers)
        act_len = len(reg_file)
        self.assertEqual(act_len, n_registers,
                         'len should be %d not %s' % (n_registers, act_len))

    def test_repr(self):
        reg_file = RegisterFile(3, prefix='R', init_values={'R1': 10, 'R2': -1})
        self.assertEqual(reg_file, eval(repr(reg_file)))
