import random
import unittest

from procsim.register import Register

class TestRegister(unittest.TestCase):
    # 'Rich comparison' tests.
    def test_lt(self):
        test_spec = {'op_str': '<',
                     'op': lambda x, y: x < y,
                     'exp_fn': lambda r1, r2: r1.read() < r2.read(),
                     'tests': {'y_above', 'y_equal', 'y_below'}}
        self.run_tests(test_spec)

    def test_le(self):
        test_spec = {'op_str': '<=',
                     'op': lambda x, y: x <= y,
                     'exp_fn': lambda r1, r2: r1.read() <= r2.read(),
                     'tests': {'y_above', 'y_equal', 'y_below'}}
        self.run_tests(test_spec)

    def test_eq(self):
        test_spec = {'op_str': '==',
                     'op': lambda x, y: x == y,
                     'exp_fn': lambda r1, r2: r1.read() == r2.read(),
                     'tests': {'y_above', 'y_equal', 'y_below'}}
        self.run_tests(test_spec)

    def test_ne(self):
        test_spec = {'op_str': '!=',
                     'op': lambda x, y: x != y,
                     'exp_fn': lambda r1, r2: r1.read() != r2.read(),
                     'tests': {'y_above', 'y_equal', 'y_below'}}
        self.run_tests(test_spec)

    def test_gt(self):
        test_spec = {'op_str': '>',
                     'op': lambda x, y: x > y,
                     'exp_fn': lambda r1, r2: r1.read() > r2.read(),
                     'tests': {'y_above', 'y_equal', 'y_below'}}
        self.run_tests(test_spec)

    def test_ge(self):
        test_spec = {'op_str': '>=',
                     'op': lambda x, y: x >= y,
                     'exp_fn': lambda r1, r2: r1.read() >= r2.read(),
                     'tests': {'y_above', 'y_equal', 'y_below'}}
        self.run_tests(test_spec)

    # Arithmetic tests.
    def test_add(self):
        test_spec = {'op_str': '+',
                     'op': lambda x, y: x + y,
                     'exp_fn': lambda r1, r2: Register(r1.read() + r2.read()),
                     'tests': {'y_above', 'y_equal', 'y_below'}}
        self.run_tests(test_spec)

    def test_sub(self):
        test_spec = {'op_str': '-',
                     'op': lambda x, y: x - y,
                     'exp_fn': lambda r1, r2: Register(r1.read() - r2.read()),
                     'tests': {'y_above', 'y_equal', 'y_below'}}
        self.run_tests(test_spec)

    # Misc tests.
    def test_write(self):
        for _ in range(100):
            reg = gen_reg()
            val = random.randint(-100000, 100000)
            reg.write(val)
            self.assertEqual(reg, Register(val),
                             '%s should have value %d after write' % (reg, val))

    def test_read(self):
        for i in range(100):
            val = random.randint(-10000, 10000)
            reg = Register(val)
            read = reg.read()
            self.assertEqual(read, val,
                             'reg.read() returned %s, should be %s' % (read, val))

    def test_repr(self):
        reg = gen_reg()
        self.assertEqual(reg, eval(repr(reg)))

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
                self.assertEqual(test_spec['op'](reg_a, reg_b.read()),
                                 expected,
                                 msg(reg_b.read()))

def gen_reg():
    """Return a Register with a random value."""
    return Register(random.randint(-100000, 100000))

def gen_reg_above(reg):
    """Return a Register with value greater than the Register argument."""
    return Register(random.randint(reg.read() + 1, reg.read() + 100000))

def gen_reg_equal(reg):
    """Return a Register with value equal to the Register argument."""
    return Register(reg.read())

def gen_reg_below(reg):
    """Return a Register with value less than the Register argument."""
    return Register(random.randint(reg.read() - 100000, reg.read() - 1))
