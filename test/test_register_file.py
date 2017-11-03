import unittest

from procsim.register_file import RegisterFile
from procsim.register import Register

class TestRegisterFile(unittest.TestCase):

    def test_eq(self):
        length = 3
        prefix = 'R'
        init_values = gen_values(length, prefix)
        reg_file = RegisterFile(length, prefix, init_values)

        for same_length in [True, False]:
            for same_prefix in [True, False]:
                for same_values in [True, False]:
                    other_length = length if same_length else length + 1
                    other_prefix = prefix if same_prefix else 'r'
                    other_values = gen_values(other_length, other_prefix)
                    if not same_values:
                        other_values[other_prefix + '0'] += 1

                    other = RegisterFile(other_length, other_prefix, other_values)

                    equality_test = self.assertFalse
                    if same_length and same_prefix and same_values:
                        equality_test = self.assertTrue

                    equality_test(reg_file == other,
                                  'same_length: %r - same_prefix: %r - same_values: %r' % (
                                      same_length, same_prefix, same_values))

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

def gen_values(length, prefix):
    """Deterministically Return valid RegisterFile init_values."""
    return {prefix + str(i): i for i in range(length)}
