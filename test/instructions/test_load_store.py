import random
import unittest

from procsim.back_end.result import Result
from procsim.instructions import Load
from procsim.memory import Memory
from procsim.register_file import RegisterFile

class TestMemoryAccess(unittest.TestCase):

    def setUp(self):
        self.register_len = 10
        init_values = {'r%d' % i: i for i in range(self.register_len)}
        self.reg_file = RegisterFile(self.register_len,
                                     init_values=init_values)
        self.memory_len = 100
        self.memory = Memory(self.memory_len)
        for i in range(len(self.memory)):
            self.memory[i] = i

    def test_load_execute(self):
        """Ensure Load returns correct Result."""
        for i in range(100):
            rd = self.random_reg()
            r1 = self.random_reg()
            r_addr = self.random_addr()
            self.reg_file[r1] = r_addr
            load = Load(rd, r1)

            exp_result = Result(rd, self.memory[r_addr])
            self.assertEqual(load.execute(self.reg_file, self.memory), exp_result)

    def random_reg(self):
        """Return a random but valid Register name."""
        return 'r%d' % random.randint(0, self.register_len - 1)

    def random_addr(self):
        """Return a random but valid Memory address."""
        return random.randint(0, len(self.memory) - 1)
