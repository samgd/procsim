import unittest

from procsim.back_end.load_store_unit import LoadStoreUnit
from procsim.back_end.result import Result
from procsim.instructions import Load
from procsim.instructions import MemoryAccess
from procsim.memory import Memory
from procsim.register_file import RegisterFile
from test.feed_log import FeedLog

class TestLoadStoreUnit(unittest.TestCase):

    def setUp(self):
        init_values = {'r%d' % i: i for i in range(10)}
        self.reg_file = RegisterFile(10, init_values=init_values)

        self.feed_log = FeedLog()

        self.memory = Memory(200)
        for i in range(len(self.memory)):
            self.memory[i] = i

    def test_correct_result_load(self):
        """Test correct load Result computed and fed by LoadStoreUnit."""
        load = Load('r0', 'r8')
        load.DELAY = 1
        unit = LoadStoreUnit(self.reg_file, self.memory, self.feed_log)
        unit.feed(load)
        unit.tick()
        unit.tick()
        self.assertEqual(self.feed_log.log, [Result('r0', 8)])

    def test_busy(self):
        """Test LoadStoreUnit busy method updates correctly after ticks."""
        load = Load('r0', 'r1')
        load.DELAY = 5

        unit = LoadStoreUnit(self.reg_file, self.memory, self.feed_log)
        self.assertFalse(unit.busy(),
                         'LoadStoreUnit should not be busy after initialization')
        unit.feed(load)
        self.assertTrue(unit.busy(),
                        'LoadStoreUnit should be busy after being fed')
        unit.trigger()
        for _ in range(load.DELAY - 1):
            unit.tick()
            self.assertTrue(unit.busy(),
                            'LoadStoreUnit should be busy before DELAY ticks')
        unit.tick()
        self.assertFalse(unit.busy(),
                         'LoadStoreUnit should not be busy after DELAY ticks')

    def test_capability(self):
        unit = LoadStoreUnit(self.reg_file, self.memory, self.feed_log)
        self.assertEqual(unit.capability(), MemoryAccess)
