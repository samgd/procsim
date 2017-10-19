import unittest

from procsim.back_end.load_store_unit import LoadStoreUnit
from procsim.instructions import MemoryAccess
from procsim.memory import Memory
from procsim.register_file import RegisterFile
from test.back_end.write_unit_stub import WriteUnitStub

class TestReservationStation(unittest.TestCase):

    def setUp(self):
        init_values = {'r%d' % i: i for i in range(10)}
        self.reg_file = RegisterFile(10, init_values=init_values)
        self.wu_stub = WriteUnitStub()
        self.memory = Memory(100)
        for i in range(len(self.memory)):
            self.memory[i] = i

    def test_capability(self):
        unit = LoadStoreUnit(self.reg_file, self.wu_stub, self.memory)
        self.assertEqual(unit.capability(), MemoryAccess)
