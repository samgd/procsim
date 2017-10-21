import unittest

from procsim.back_end.load_store_unit import LoadStoreUnit
from procsim.back_end.result import Result
from procsim.instructions import Load
from procsim.instructions import MemoryAccess
from procsim.memory import Memory
from procsim.register_file import RegisterFile
from test.back_end.write_unit_stub import WriteUnitStub

class TestLoadStoreUnit(unittest.TestCase):

    def setUp(self):
        init_values = {'r%d' % i: i for i in range(10)}
        self.reg_file = RegisterFile(10, init_values=init_values)

        self.wu_stub = WriteUnitStub()

        self.memory = Memory(200)
        for i in range(len(self.memory)):
            self.memory[i] = i

    def test_correct_result_load(self):
        """Test correct load Result computed by LoadStoreUnit and fed to WriteUnit."""
        load = Load('r0', 'r8')
        load.DELAY = 1
        unit = LoadStoreUnit(self.reg_file, self.wu_stub, self.memory)
        unit.feed(load)
        unit.tick()
        unit.tick()
        self.assertEqual(self.wu_stub.result, Result('r0', 8))

    def test_busy(self):
        """Test LoadStoreUnit busy method updates correctly after ticks."""
        load = Load('r0', 'r1')
        load.DELAY = 5

        unit = LoadStoreUnit(self.reg_file, self.wu_stub, self.memory)
        self.assertFalse(unit.busy(),
                         'LoadStoreUnit busy after initialization')
        unit.feed(load)
        self.assertTrue(unit.busy(),
                        'LoadStoreUnit not busy after being fed')
        for _ in range(load.DELAY - 1):
            unit.tick()
            self.assertTrue(unit.busy(),
                            'LoadStoreUnit not busy before DELAY ticks')
        unit.tick()
        self.assertFalse(unit.busy(),
                         'LoadStoreUnit busy after DELAY ticks')

    def test_capability(self):
        unit = LoadStoreUnit(self.reg_file, self.wu_stub, self.memory)
        self.assertEqual(unit.capability(), MemoryAccess)
