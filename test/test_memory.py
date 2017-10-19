import random
import unittest

from procsim.memory import Memory
from procsim.register import Register

class TestMemory(unittest.TestCase):

    def test_len(self):
        for _ in range(100):
            size = random.randint(-10000, 0)
            with self.assertRaises(ValueError):
                Memory(size)
        for _ in range(100):
            size = random.randint(1, 10000)
            memory = Memory(size)
            self.assertEqual(len(memory), size)

    def test_init_values(self):
        size = 200
        memory = Memory(size)
        for i in range(size):
            self.assertEqual(memory[i], None)

    def test_get_set_validate(self):
        size = 200
        memory = Memory(size)
        for invalid_type in ['foo', None, {1}]:
            with self.assertRaises(TypeError):
                temp = memory[invalid_type]
            with self.assertRaises(TypeError):
                memory[invalid_type] = 5
        for _ in range(100):
            invalid_idx = random.randint(-10000, -1)
            with self.assertRaises(IndexError):
                temp = memory[invalid_idx]
            with self.assertRaises(IndexError):
                memory[invalid_idx] = 5

    def test_get_set_valid(self):
        for size in [100, 4000, 10000]:
            memory = Memory(size)
            for i in range(100):
                new_value = random.randint(-10000, 10000)
                address = random.randint(0, size - 1)
                # Test using addresses stored in Registers 50% of the time.
                if i % 2 == 0:
                    address = Register(address)
                memory[address] = new_value
                self.assertEqual(memory[address], new_value)
