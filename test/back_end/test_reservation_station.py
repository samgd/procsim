import random
import unittest

from procsim.back_end.reservation_station import ReservationStation
from procsim.back_end.execution_unit import ExecutionUnit
from procsim.clock import Clock
from procsim.instructions import Add
from procsim.instructions import AddI
from procsim.instructions import Instruction

class TestReservationStation(unittest.TestCase):

    def setUp(self):
        self.clock = Clock()
        self.rs = ReservationStation(capacity=200)
        self.iu = IntegerUnitStub()
        self.clock.register(self.rs)
        self.clock.register(self.iu)

    def test_invalid_capacity(self):
        """Test exception thrown when initialized with invalid capacity."""
        for _ in range(100):
            invalid = random.randint(-1000, 0)
            with self.assertRaises(ValueError):
                ReservationStation(capacity=invalid)

    def test_feed_busy(self):
        """Test busy operation when feeding Instructions."""
        for capacity in [1, 5, 25, 200]:
            rs = ReservationStation(capacity=capacity)
            for _ in range(capacity):
                self.assertFalse(rs.busy(),
                                 'ReservationStation should not be busy after < capacity feeds')
                rs.feed(Add('r0', 'r1', 'r2'))
            self.assertTrue(rs.busy(),
                            'ReservationStation should be busy after capacity feeds')
            with self.assertRaises(AssertionError):
                rs.feed(Add('r1', 'r2', 'r3'))

    def test_tick_no_execution_units(self):
        """Ensure error raised when no ExecutionUnits exist for an Instruction."""
        # Feed Instruction and tick to move it from future to current state.
        self.rs.feed(Add('r0', 'r1', 'r2'))
        self.rs.tick()
        with self.assertRaises(AssertionError):
            self.rs.tick()

    def test_instruction_passthrough_one_feed_one_execution(self):
        """Test one Instruction passes through ReservationStation OK."""
        self.rs.register(self.iu)

        instruction = AddI('r0', 'r1', 10)
        self.rs.feed(instruction)
        self.clock.tick()
        self.assertSetEqual(self.iu.received, set())

        self.clock.tick()
        self.assertSetEqual(self.iu.received, set([instruction]))

    def test_instruction_passthrough_sequential_feed_one_execution(self):
        """Test sequential Instruction feeds pass through ReservationStation OK."""
        self.rs.register(self.iu)

        fed_instructions = set()
        last_feed = None
        for i in range(100):
            # Skip feeding occasionally to insert bubbles into the pipeline.
            if not i % 7 == 0:
                last_feed = AddI('r0', 'r1', i)
                self.rs.feed(last_feed)
                fed_instructions.add(last_feed)
            else:
                last_feed = None
            self.clock.tick()
            # ReservationStation has a 1 cycle delay - not expecting to receive
            # last instruction fed out until next cycle.
            exp_received = fed_instructions - set([last_feed])
            self.assertEqual(self.iu.received, exp_received)

        self.clock.tick()
        self.assertEqual(self.iu.received, fed_instructions)

    def test_instruction_passthrough_many_feed_one_exeuction(self):
        """Test many Instructions fed first then pass through OK."""
        self.rs.register(self.iu)

        num_inst = 100
        fed_instructions = set()
        for i in range(num_inst):
            instruction = AddI('r0', 'r1', i)
            self.rs.feed(instruction)
            fed_instructions.add(instruction)
        self.clock.tick()

        for i in range(num_inst):
            self.clock.tick()
        self.assertEqual(self.iu.received, fed_instructions)

class IntegerUnitStub(ExecutionUnit):
    """Stub that logs instructions fed. Can receive 1 Instruction per tick.

    Attributes:
        received: Set containing all Instructions that have been arguments to
        feed calls.
    """

    def __init__(self):
        self.received = set()
        self.fed = False

    def capability(self):
        return Instruction

    def feed(self, instruction):
        self.received.add(instruction)
        self.fed = True

    def busy(self):
        return self.fed

    def operate(self):
        pass

    def trigger(self):
        self.fed = False
