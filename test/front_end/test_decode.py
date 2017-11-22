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

        self.decode = decode.Decode(self.feed_log)
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
            self.decode.DELAY = delay
            exp_log = []
            self.feed_log.log = []
            for (act_ins, exp_ins) in self.test_strs:
                self.decode.feed(act_ins)
                self.decode.tick() # Fed ins_str becomes current state.
                for _ in range(self.decode.DELAY):
                    # Check Instruction not output before DELAY ticks.
                    self.assertTrue(instruction_list_equal(self.feed_log.log, exp_log))
                    self.decode.tick()
                exp_log.append(exp_ins)
                if isinstance(exp_ins, ins.Blth):
                    exp_log[-1].branch_info = act_ins['branch_info']
                self.assertTrue(instruction_list_equal(self.feed_log.log, exp_log))

    def test_full(self):
        """Test IntegerUnit full method updates correctly after ticks."""
        for delay in [1, 2, 5, 10]:
            self.decode.DELAY = delay
            for ins, _ in self.test_strs:
                self.assertFalse(self.decode.full(),
                                 'Decode should not be full after initialization')
                self.decode.feed(ins)
                self.assertTrue(self.decode.full(),
                                'Decode should be full after being fed')
                for _ in range(self.decode.DELAY):
                    self.decode.tick()
                    self.assertTrue(self.decode.full(),
                                    'Decode should be full before DELAY ticks')
                self.decode.tick()
                self.assertFalse(self.decode.full(),
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

        self.decode.feed(self.test_strs[0])
        self.assertTrue(self.decode.full(),
                        'Decode should be full after being fed')
        self.decode.flush()
        self.assertFalse(self.decode.full(),
                         'Decode should not be full after flush')
        self.assertEqual(log.n_flush, 1, 'Decode must flush ReorderBuffer')
