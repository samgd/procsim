import random
import unittest

from procsim.back_end.result import Result
from procsim.back_end.write_unit import WriteUnit
from procsim.instructions import Instruction
from procsim.memory import Memory
from procsim.register import Register
from procsim.register_file import RegisterFile

class TestWriteUnit(unittest.TestCase):

    def setUp(self):
        self.register_len = 10
        init_values = {'r%d' % i: i for i in range(self.register_len)}
        self.reg_file = RegisterFile(self.register_len, init_values=init_values)
        self.memory = Memory(100)

    def test_correct_write(self):
        """Ensure value written to destination."""
        unit = WriteUnit(self.reg_file, self.memory, write_delay=1)
        for _ in range(100):
            typ = random.choice([Register, Memory])
            dest = self.random_reg() if typ == Register else self.random_addr()
            value = random.randint(-10000, 10000)

            result = Result(dest, value, typ)
            unit.feed(result)
            unit.trigger() # Result becomes current_state.
            unit.tick() # Write Result value to dest.

            act_value = self.reg_file[dest] if typ == Register else self.memory[dest]
            self.assertEqual(act_value, value)

    def test_feed_write_delay(self):
        """Test write occurs after given write_delay."""
        result = Result('r0', 10)
        for write_delay in [1, 5, 10]:
            # Initialize WriteUnit.
            unit = WriteUnit(self.reg_file, self.memory, write_delay)

            unit.feed(result)
            unit.tick()
            self.assertNotEqual(self.reg_file[result.dest], result.value,
                                'RegisterFile updated before write_delay')
            # Perform write_delay - 1 ticks.
            for _ in range(write_delay - 1):
                unit.tick()
                self.assertNotEqual(self.reg_file[result.dest], result.value,
                                    'RegisterFile updated before write_delay')
            # Call tick to trigger write.
            unit.tick()
            self.assertEqual(self.reg_file[result.dest], result.value,
                             'RegisterFile not updated after write_delay')
            # Reset RegisterFile.
            self.reg_file[result.dest] = 0

    def test_feed_full(self):
        """Test full returns True after feed and False after write_delay."""
        result = Result('r0', 10)
        for write_delay in [1, 5, 10]:
            unit = WriteUnit(self.reg_file, self.memory, write_delay)
            self.assertFalse(unit.full(),
                             'WriteUnit should not be full after initialization')
            unit.feed(result)
            self.assertTrue(unit.full(),
                            'WriteUnit should be full after being fed')
            unit.trigger()
            for _ in range(write_delay - 1):
                unit.tick()
                self.assertTrue(unit.full(),
                                'WriteUnit should be full before write_delay ticks')
            unit.tick()
            self.assertFalse(unit.full(),
                             'WriteUnit should not be full after write_delay ticks %d')

    def test_capability(self):
        unit = WriteUnit(self.reg_file, self.memory)
        self.assertEqual(unit.capability(), Result)

    def random_reg(self):
        """Return a random but valid Register name."""
        return 'r%d' % random.randint(0, self.register_len - 1)

    def random_addr(self):
        """Return a random but valid Memory address."""
        return random.randint(0, len(self.memory) - 1)
