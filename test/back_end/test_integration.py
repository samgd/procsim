import unittest

from procsim.back_end.integer_unit import IntegerUnit
from procsim.back_end.load_store_queue import LoadStoreQueue
from procsim.back_end.reorder_buffer import ReorderBuffer
from procsim.back_end.reservation_station import ReservationStation
from procsim.clock import Clock
from procsim.front_end.instructions import Add
from procsim.front_end.instructions import AddI
from procsim.front_end.instructions import Load
from procsim.front_end.instructions import Store
from procsim.memory import Memory
from procsim.register_file import RegisterFile
from test.back_end.bus_log import BusLog

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.clock = Clock()
        self.bus = BusLog()

        self.memory = Memory(10)
        for i in range(len(self.memory)):
            self.memory[i] = i

        self.n_gpr = 6
        self.rf = RegisterFile(self.n_gpr, 'r',
                               init_values={'r%d' % i: i for i in range(self.n_gpr)})
        iu1 = IntegerUnit(self.bus)
        iu2 = IntegerUnit(self.bus)
        iu3 = IntegerUnit(self.bus)

        rs = ReservationStation()
        rs.register(iu1)
        rs.register(iu2)
        rs.register(iu3)

        lsq = LoadStoreQueue(self.memory, self.bus)

        self.rob = ReorderBuffer(self.rf, rs, lsq)

        self.clock.register(self.rob)
        self.clock.register(lsq)
        self.clock.register(rs)
        self.clock.register(iu3)
        self.clock.register(iu2)
        self.clock.register(iu1)

        self.bus.subscribe(self.rob)
        self.bus.subscribe(rs)
        self.bus.subscribe(lsq)

    def test_straightline_integration(self):
        instructions = [Add('r2', 'r3', 'r4'),
                        Store('r1', 'r2'),
                        Load('r1', 'r2'),
                        AddI('r1', 'r1', 1),
                        Store('r1', 'r2')]
        for ins in instructions:
            self.rob.feed(ins)

        # Enough clock ticks to ensure completion.
        for _ in range(100):
            self.clock.tick()

        self.assertListEqual([self.rf['r%d' % i] for i in range(self.n_gpr)],
                             [0, 2, 7, 3, 4, 5])
        self.assertListEqual([self.memory[i] for i in range(len(self.memory))],
                             [0, 1, 2, 3, 4, 5, 6, 2, 8, 9])
