import math
import random
import unittest

from procsim.back_end.reorder_buffer import ReorderBuffer
from procsim.back_end.reservation_station import ReservationStation
from procsim.back_end.result import Result
from procsim.front_end.instructions.add import Add
from procsim.register_file import RegisterFile
from test.feed_log import FeedLog

class TestReorderBuffer(unittest.TestCase):

    def setUp(self):
        self.n_gpr_registers = 31
        self.rf = RegisterFile(self.n_gpr_registers)
        self.log = FeedLog()
        self.generate_add = lambda cap: Add('r%d' % random.randint(0, cap - 1),
                                        'r%d' % random.randint(0, cap - 1),
                                        'r%d' % random.randint(0, cap - 1))

    def test_invalid_capacity(self):
        """Test exception thrown when initialized with invalid capacity."""
        for _ in range(100):
            invalid = random.randint(-1000, 0)
            with self.assertRaises(ValueError):
                ReorderBuffer(self.rf, self.log, capacity=invalid)

    def test_feed_full(self):
        """Test full operation when feeding Instructions."""
        for rob_capacity in [1, 5, 25, 200]:
            for rs_capacity in [1, 5, 25, 200]:
                limit = min(rob_capacity, rs_capacity)
                rs = ReservationStation(capacity=rs_capacity)
                rob = ReorderBuffer(self.rf, rs, capacity=rob_capacity)
                for _ in range(limit):
                    self.assertFalse(rob.full(),
                                     'ReorderBuffer should not be full after < %d feeds' % limit)
                    rob.feed(self.generate_add(self.n_gpr_registers))
                self.assertTrue(rob.full(),
                                'ReorderBuffer should be full after %d feeds' % limit)
                with self.assertRaises(AssertionError):
                    rob.feed(self.generate_add(self.n_gpr_registers))

    def test_get_queue_id(self):
        """Test that _get_queue_id throws an error on wrap-around."""
        for capacity in [1, 5, 25, 200]:
            rob = ReorderBuffer(self.rf, self.log, capacity=capacity)
            for _ in range(capacity):
                rob._get_queue_id()
            with self.assertRaises(AssertionError):
                rob._get_queue_id()

    def test_instructions_removed_from_queue_on_commit(self):
        """Test that commit frees a slot in the ROB."""
        for capacity in [1, 5, 25, 200]:
            log = FeedLog()
            rob = ReorderBuffer(self.rf, log, capacity=capacity)
            # Half fill.
            for _ in range(capacity // 2):
                rob.feed(self.generate_add(self.n_gpr_registers))
            rob.tick() # Instructions now in current queue.
            # Remove all fed from ROB queue by giving values.
            self.assertEqual(capacity // 2, len(log.log))
            for ins in log.log:
                rob.receive(Result(ins.tag, 5))
            for _ in range(math.ceil(capacity / rob.WIDTH)):
                rob.tick()
            # Should now be able to feed capacity instructions.
            for _ in range(capacity):
                rob.feed(self.generate_add(self.n_gpr_registers))

    def test_inorder_commit(self):
        """Ensure instruction Results are committed in-order."""
        for _ in range(30):
            for capacity in [1, 5, 25, 200]:
                # Initialize test components.
                self.log.reset()
                act_rf = RegisterFile(capacity,
                                      init_values={'r%d' % i: 0 for i in range(capacity)})
                exp_rf = RegisterFile(capacity,
                                      init_values={'r%d' % i: 0 for i in range(capacity)})
                rob = ReorderBuffer(act_rf, self.log, capacity)
                rob.WIDTH = random.randint(1, 2*capacity)

                # Feed instructions into ROB.
                n_ins = random.randint(1, capacity)
                register_names = []
                for i in range(n_ins):
                    add = self.generate_add(capacity)
                    register_names.append(add.rd)
                    rob.feed(add)
                rob.tick()

                # Generate a Result value for each fed instruction.
                result_vals = [random.randint(1, 10000) for _ in range(n_ins)]

                # Publish all but first result in reverse order to ROB. Should be
                # no updates to act_rf as the first instruction is stalled!
                for i in reversed(range(1, n_ins)):
                    rob.receive(Result(self.log.log[i].tag, result_vals[i]))
                    rob.tick()
                    self.assertEqual(exp_rf, act_rf)

                # Publish result of first instruction - all can now be comitted in
                # turn.
                rob.receive(Result(self.log.log[0].tag, result_vals[0]))

                # Group updates into ROB width chunks.
                updates = list(zip(register_names, result_vals))
                group_updates = [updates[i:i + rob.WIDTH]
                                 for i in range(0, len(updates), rob.WIDTH)]

                # Ensure in-order commit of width instructions per tick.
                for group in group_updates:
                    rob.tick()
                    for (name, result) in group:
                        exp_rf[name] = result
                    self.assertEqual(exp_rf, act_rf)
                rob.tick()
