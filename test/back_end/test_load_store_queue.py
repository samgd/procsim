import random
import unittest

from procsim.back_end.instructions.load import Load
from procsim.back_end.instructions.store import Store
from procsim.back_end.load_store_queue import LoadStoreQueue
from procsim.back_end.result import Result
from procsim.memory import Memory
from test.back_end.bus_log import BusLog

class TestLoadStoreQueue(unittest.TestCase):

    def setUp(self):
        self.memory = Memory(128)
        self.bus = BusLog()

    def test_invalid_capacity(self):
        """Test exception thrown when initialized with invalid capacity."""
        for _ in range(100):
            invalid = random.randint(-1000, 0)
            with self.assertRaises(ValueError):
               LoadStoreQueue(self.memory, self.bus, invalid)

    def test_feed_full(self):
        """Test full method when feeding Instructions."""
        for capacity in [1, 5, 25, 200]:
            lsq = LoadStoreQueue(self.memory, self.bus, capacity)
            for _ in range(capacity):
                self.assertFalse(lsq.full(),
                                 'LoadStoreQueue should not be full after < %d feeds' % capacity)
                lsq.feed(self.generate_load(capacity))
            self.assertTrue(lsq.full(),
                            'LoadStoreQueue should be full after %d feeds' % capacity)
            with self.assertRaises(AssertionError):
                lsq.feed(self.generate_load(capacity))

    def test_instructions_receive_published_results(self):
        """Test Instructions receive published results OK."""
        load = Load('ROB1', 'ROB2')
        store = Store('ROB3', 'ROB4', 'ROB2')
        lsq = LoadStoreQueue(self.memory, self.bus, 32)
        lsq.feed(load)
        lsq.feed(store)
        lsq.tick()

        lsq.receive(Result('ROB2', 10))
        self.assertEqual(load.address, 10)
        self.assertEqual(store.value, 10)

    def test_load_execute_correct_result_and_delay(self):
        """Test that the correct Load Result is published after DELAY ticks."""
        for _ in range(50):
            for delay in [1, 5, 25, 200]:
                self.bus.reset()
                load = Load('ROB1', random.randint(0, 127))
                load.DELAY = delay
                lsq = LoadStoreQueue(self.memory, self.bus, 32)
                self.memory[load.address] = random.randint(0, 10000)
                lsq.feed(load)
                for _ in range(delay):
                    lsq.tick()
                    self.assertListEqual(self.bus.log, [])
                lsq.tick()
                self.assertListEqual(self.bus.log,
                                     [load.execute(self.memory)])

    def test_store_execute_correct_result_no_delay(self):
        """Test that the correct Store Result is published - no delay req."""
        for _ in range(50):
            for delay in [1, 5, 25, 200]:
                self.bus.reset()
                store = Store('ROB1',
                              random.randint(0, len(self.memory) - 1),
                              random.randint(1, 10000))
                store.DELAY = delay # Should not matter at this stage.
                lsq = LoadStoreQueue(self.memory, self.bus, 32)
                self.memory[store.address] = 0 # Should not be changed!
                lsq.feed(store)
                lsq.tick()
                lsq.tick()
                self.assertEqual(self.memory[store.address], 0,
                                 'Store execute should not change memory')
                self.assertListEqual(self.bus.log,
                                     [store.execute()])

    def test_inorder_execute(self):
        """Ensure Instructions are executed in-order."""
        capacity = 16
        lsq = LoadStoreQueue(self.memory, self.bus, capacity)
        # Fill LSQ with MemoryAccess Instructions.
        instructions = []
        for _ in range(capacity):
            ins = self.generate_memory_access(capacity)
            instructions.append(ins)
            lsq.feed(ins)
        lsq.tick()
        # Ensure all execute dependencies are met.
        for i in range(capacity):
            lsq.receive(Result('ROB%d' % i, i))
        # Tick max # times req. for all Instructions to have completed.
        for _ in range(sum([ins.DELAY for ins in instructions])):
            lsq.tick()
        # Compute expected sequence of Results published by LoadStoreQueue.
        exp_results = []
        for ins in instructions:
            if isinstance(ins, Load):
                exp_results.append(ins.execute(self.memory))
            else:
                exp_results.append(ins.execute())
        self.assertListEqual(self.bus.log, exp_results)

    def generate_memory_access(self, capacity):
        generator = random.choice([self.generate_load,
                                   self.generate_store])
        return generator(capacity)

    def generate_load(self, capacity):
        return Load('ROB%d' % random.randint(0, capacity - 1),
                    'ROB%d' % random.randint(0, capacity - 1))

    def generate_store(self, capacity):
        return Store('ROB%d' % random.randint(0, capacity - 1),
                     'ROB%d' % random.randint(0, capacity - 1),
                     'ROB%d' % random.randint(0, capacity - 1))
