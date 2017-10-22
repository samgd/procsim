import random
import unittest

from procsim.back_end.reservation_station import ReservationStation
from procsim.instructions import Add
from procsim.instructions import AddI
from procsim.instructions import Instruction
from test.feed_log import FeedLog

class TestReservationStation(unittest.TestCase):

    def setUp(self):
        self.rs = ReservationStation(capacity=200)
        self.feed_log = FeedLog()
        self.feed_log.capability = lambda: Instruction
        self.rs.register(self.feed_log)

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
        instruction = AddI('r0', 'r1', 10)
        self.rs.feed(instruction)
        self.rs.tick()
        self.assertListEqual(self.feed_log.log, [])

        self.rs.tick()
        self.assertListEqual(self.feed_log.log, [instruction])

    def test_instruction_passthrough_sequential_feed_one_execution(self):
        """Test sequential Instruction feeds pass through ReservationStation OK."""
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
            self.rs.tick()
            # ReservationStation has a 1 cycle delay - not expecting to receive
            # last instruction fed out until next cycle.
            exp_received = fed_instructions - set([last_feed])
            self.assertEqual(set(self.feed_log.log), exp_received)

        self.rs.tick()
        self.assertEqual(set(self.feed_log.log), fed_instructions)

    def test_instruction_passthrough_many_feed_one_exeuction(self):
        """Test many Instructions fed first then pass through OK."""
        num_inst = 100
        fed_instructions = set()
        for i in range(num_inst):
            instruction = AddI('r0', 'r1', i)
            self.rs.feed(instruction)
            fed_instructions.add(instruction)
        self.rs.tick()

        for i in range(num_inst):
            self.rs.tick()
        self.assertEqual(set(self.feed_log.log), fed_instructions)
