import unittest

from procsim.front_end.branch_info import BranchInfo
from procsim.front_end import decode
from test.feed_log import FeedLog
from test.flushable_log import FlushableLog
from test.front_end.utils import instruction_list_equal
import procsim.front_end.instructions as ins

class TestDecode(unittest.TestCase):

    def setUp(self):
        self.feed_log = FeedLog()
        # ReorderBuffer full method takes a param. Modify FeedLog to ignore it.
        self.feed_log._full = self.feed_log.full
        self.feed_log.full = lambda x: self.feed_log._full()

        self.test_strs = [('add r1 r2 r3', ins.Add('r1', 'r2', 'r3')),
                          ('addi r1 r2 5', ins.AddI('r1', 'r2', 5)),
                          ('sub rd r0 r9', ins.Sub('rd', 'r0', 'r9')),
                          ('subi r1 r2 10', ins.SubI('r1', 'r2', 10)),
                          ('ldr r0 r1', ins.Load('r0', 'r1')),
                          ('str r99 r100', ins.Store('r99', 'r100')),
                          ('j 1000', ins.Jump(1000)),
                          ('blth r1 r2 10', ins.Blth('r1', 'r2', 10))]
        self.test_strs = [({'instruction_str': ins_str}, exp_ins)
                          for (ins_str, exp_ins) in self.test_strs]
        self.test_strs[7][0]['branch_info'] = BranchInfo(False, 10, 9)

    def test_correct_result(self):
        """Test correct Result computed and fed by Decode stage."""
        for delay in [1, 2, 5, 10]:
            self.feed_log.reset()
            unit = decode.Decode(self.feed_log)
            unit.DELAY = delay
            exp_log = []
            self.feed_log.log = []
            for (act_ins, exp_ins) in self.test_strs:
                unit.feed(act_ins)
                unit.tick() # Fed ins_str becomes current state.
                for _ in range(unit.DELAY):
                    # Check Instruction not output before DELAY ticks.
                    self.assertTrue(instruction_list_equal(self.feed_log.log, exp_log))
                    unit.tick()
                exp_log.append(exp_ins)
                if isinstance(exp_ins, ins.Blth):
                    exp_log[-1].branch_info = act_ins['branch_info']
                self.assertTrue(instruction_list_equal(self.feed_log.log, exp_log))

    def test_full(self):
        """Test Decode full method updates correctly after ticks."""
        test_ins = self.test_strs[0][0]

        for capacity in [1, 5, 10]:
            for delay in [1, 2, 5, 10]:
                unit = decode.Decode(self.feed_log, capacity=capacity)
                unit.DELAY = delay

                self.assertFalse(unit.full(),
                                 'Decode should not be full after initialization')
                for _ in range(capacity):
                    unit.feed(test_ins)
                self.assertTrue(unit.full(),
                                'Decode should be full after being fed')
                for i in range(unit.DELAY):
                    unit.tick()
                    self.assertTrue(unit.full(),
                                    'Decode should be full before DELAY ticks %r %r')
                unit.tick()
                self.assertFalse(unit.full(),
                                 'Decode should not be full after DELAY ticks')

    def test_decode_str(self):
        for act_ins, exp_ins in self.test_strs:
            if isinstance(exp_ins, ins.Blth):
                exp_ins.branch_info = act_ins['branch_info']
            self.assertTrue(instruction_list_equal([decode._decode(act_ins)],
                                                   [exp_ins]))

    def test_flush(self):
        """Ensure flush flushes Decode and ReorderBuffer."""
        log = FlushableLog()
        self.feed_log.flush = log.flush

        unit = decode.Decode(self.feed_log, capacity=1)

        unit.feed(self.test_strs[0][0])
        self.assertTrue(unit.full(),
                        'Decode should be full after being fed')
        unit.flush()
        self.assertFalse(unit.full(),
                         'Decode should not be full after flush')
        self.assertEqual(log.n_flush, 1, 'Decode must flush ReorderBuffer')

    def test_superscalar(self):
        """Ensure up to width instructions are issued per cycle."""
        for capacity in [1, 5, 10, 200]:
            for width in [1, 4, 16]:
                n_full = min(capacity, width)

                for n_feed in range(1, n_full + 1):
                    for delay in [1, 5, 10]:
                        self.feed_log.reset()
                        unit = decode.Decode(self.feed_log, capacity=capacity, width=width)
                        unit.DELAY = delay

                        exp_ins = []
                        for i in range(n_feed):
                            act, exp = self.test_strs[i % (len(self.test_strs) - 1)]
                            unit.feed(act)
                            exp_ins.append(exp)

                        unit.tick() # Change to current queue.
                        for _ in range(delay):
                            unit.tick() # Issue all fed.

                        self.assertTrue(instruction_list_equal(self.feed_log.log, exp_ins))
