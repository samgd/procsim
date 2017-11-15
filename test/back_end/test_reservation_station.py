import random
import unittest

from procsim.back_end.instructions.instruction import Instruction
from procsim.back_end.instructions.integer_logical import IntegerLogical
from procsim.back_end.reservation_station import ReservationStation
from procsim.back_end.result import Result
from test.feed_log import FeedLog

class TestReservationStation(unittest.TestCase):

    def setUp(self):
        self.rs = ReservationStation(capacity=200)
        self.feed_log = FeedLog()
        self.feed_log.capability = lambda: Instruction
        self.generate_add = lambda: IntegerLogical('ROB1',
                                                   lambda o1, o2: o1 + o2,
                                                   random.randint(-100, 100),
                                                   random.randint(-100, 100))

    def test_invalid_capacity(self):
        """Test exception thrown when initialized with invalid capacity."""
        for _ in range(100):
            invalid = random.randint(-1000, 0)
            with self.assertRaises(ValueError):
                ReservationStation(capacity=invalid)

    def test_feed_full(self):
        """Test full operation when feeding Instructions."""
        self.rs.register(self.feed_log)
        for capacity in [1, 5, 25, 200]:
            rs = ReservationStation(capacity=capacity)
            for _ in range(capacity):
                self.assertFalse(rs.full(),
                                 'ReservationStation should not be full after < capacity feeds')
                rs.feed(self.generate_add())
            self.assertTrue(rs.full(),
                            'ReservationStation should be full after capacity feeds')
            with self.assertRaises(AssertionError):
                rs.feed(self.generate_add())

    def test_tick_no_execution_units(self):
        """Ensure error raised when no ExecutionUnits exist for an Instruction."""
        # Feed Instruction and tick to move it from future to current state.
        self.rs.feed(self.generate_add())
        self.rs.trigger()
        with self.assertRaises(AssertionError):
            self.rs.tick()

    def test_instruction_passthrough_one_feed_one_execution(self):
        """Test one Instruction passes through ReservationStation OK."""
        self.rs.register(self.feed_log)
        instruction = self.generate_add()
        self.rs.feed(instruction)
        self.rs.tick()
        self.assertListEqual(self.feed_log.log, [])

        self.rs.tick()
        self.assertListEqual(self.feed_log.log, [instruction])

    def test_instruction_passthrough_sequential_feed_one_execution(self):
        """Test sequential Instruction feeds pass through ReservationStation OK."""
        self.rs.register(self.feed_log)
        fed_instructions = set()
        last_feed = None
        for i in range(100):
            # Skip feeding occasionally to insert bubbles into the pipeline.
            if not i % 7 == 0:
                last_feed = self.generate_add()
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

    def test_instruction_passthrough_many_feed_one_execution(self):
        """Test many Instructions fed first then pass through OK."""
        self.rs.register(self.feed_log)
        num_inst = 100
        fed_instructions = set()
        for i in range(num_inst):
            instruction = self.generate_add()
            self.rs.feed(instruction)
            fed_instructions.add(instruction)
        self.rs.tick()

        for i in range(num_inst):
            self.rs.tick()
        self.assertEqual(set(self.feed_log.log), fed_instructions)

    def test_instructions_receive_published_results(self):
        """Test Instructions receive published results and dispatch OK."""
        ins = IntegerLogical('ROB1', lambda o1, o2: o1 - o2, 'ROB2', 'ROB3')
        self.rs.register(self.feed_log)

        self.rs.feed(ins)
        self.rs.trigger()

        self.rs.receive(Result('ROB4', 100))
        self.rs.tick()
        self.assertListEqual(self.feed_log.log, [])

        self.rs.receive(Result('ROB3', 100))
        self.rs.tick()
        self.assertListEqual(self.feed_log.log, [])

        self.rs.receive(Result('ROB2', 50))
        self.rs.tick()
        self.assertListEqual(self.feed_log.log, [ins])
