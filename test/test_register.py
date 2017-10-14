import random
import unittest

from procsim.register import Register

class TestRegister(unittest.TestCase):
    # 'Rich comparison' tests.
    def test_lt(self):
        test_spec = {'op_str': '<',
                     'op': lambda x, y: x < y,
                     'exp_fn': lambda r1, r2: r1.value < r2.value,
                     'tests': {'y_above', 'y_equal', 'y_below'}}
        self.run_tests(test_spec)

    def test_le(self):
        test_spec = {'op_str': '<=',
                     'op': lambda x, y: x <= y,
                     'exp_fn': lambda r1, r2: r1.value <= r2.value,
                     'tests': {'y_above', 'y_equal', 'y_below'}}
        self.run_tests(test_spec)

    def test_eq(self):
        test_spec = {'op_str': '==',
                     'op': lambda x, y: x == y,
                     'exp_fn': lambda r1, r2: r1.value == r2.value,
                     'tests': {'y_above', 'y_equal', 'y_below'}}
        self.run_tests(test_spec)

    def test_ne(self):
        test_spec = {'op_str': '!=',
                     'op': lambda x, y: x != y,
                     'exp_fn': lambda r1, r2: r1.value != r2.value,
                     'tests': {'y_above', 'y_equal', 'y_below'}}
        self.run_tests(test_spec)

    def test_gt(self):
        test_spec = {'op_str': '>',
                     'op': lambda x, y: x > y,
                     'exp_fn': lambda r1, r2: r1.value > r2.value,
                     'tests': {'y_above', 'y_equal', 'y_below'}}
        self.run_tests(test_spec)

    def test_ge(self):
        test_spec = {'op_str': '>=',
                     'op': lambda x, y: x >= y,
                     'exp_fn': lambda r1, r2: r1.value >= r2.value,
                     'tests': {'y_above', 'y_equal', 'y_below'}}
        self.run_tests(test_spec)

    # Arithmetic tests.
    def test_add(self):
        test_spec = {'op_str': '+',
                     'op': lambda x, y: x + y,
                     'exp_fn': lambda r1, r2: Register(r1.value + r2.value),
                     'tests': {'y_above', 'y_equal', 'y_below'}}
        self.run_tests(test_spec)

    def test_sub(self):
        test_spec = {'op_str': '-',
                     'op': lambda x, y: x - y,
                     'exp_fn': lambda r1, r2: Register(r1.value - r2.value),
                     'tests': {'y_above', 'y_equal', 'y_below'}}
        self.run_tests(test_spec)

    # Test utilities.
    def run_tests(self, test_spec):
        """Run tests based on a test specification."""
        for _ in range(100):
            for test in test_spec['tests']:
                reg_a = gen_reg()
                if test == 'y_above':
                    reg_b = gen_reg_above(reg_a)
                elif test == 'y_equal':
                    reg_b = gen_reg_equal(reg_a)
                elif test == 'y_below':
                    reg_b = gen_reg_below(reg_a)
                else:
                    raise ValueError('unknown test "%s"' % test)

                expected = test_spec['exp_fn'](reg_a, reg_b)
                def msg(test_val, reg=reg_a, exp=expected):
                    return '%s %s %s should be %s' % (reg,
                                                      test_spec['op_str'],
                                                      test_val,
                                                      exp)

                self.assertEqual(test_spec['op'](reg_a, reg_b),
                                 expected,
                                 msg(reg_b))
                self.assertEqual(test_spec['op'](reg_a, reg_b.value),
                                 expected,
                                 msg(reg_b.value))

def gen_reg():
    """Return a Register with a random value."""
    return Register(random.randint(-100000, 100000))

def gen_reg_above(reg):
    """Return a Register with value greater than the Register argument."""
    return Register(random.randint(reg.value + 1, reg.value + 100000))

def gen_reg_equal(reg):
    """Return a Register with value equal to the Register argument."""
    return Register(reg.value)

def gen_reg_below(reg):
    """Return a Register with value less than the Register argument."""
    return Register(random.randint(reg.value - 100000, reg.value - 1))
