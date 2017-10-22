import unittest

from procsim.front_end import decode
from test.feed_log import FeedLog
from test.front_end.utils import instruction_list_equal
import procsim.instructions as ins

class TestDecode(unittest.TestCase):

    def setUp(self):
        self.feed_log = FeedLog()
        self.decode = decode.Decode(self.feed_log)
        self.test_strs = [('add r1 r2 r3', ins.Add('r1', 'r2', 'r3')),
                          ('addi r1 r2 5', ins.AddI('r1', 'r2', 5)),
                          ('sub rd r0 r9', ins.Sub('rd', 'r0', 'r9')),
                          ('subi r1 r2 10', ins.SubI('r1', 'r2', 10)),
                          ('ldr r0 r1', ins.Load('r0', 'r1')),
                          ('str r99 r100', ins.Store('r99', 'r100')),
                          ('j 1000', ins.Jump(1000)),
                          ('blth r1 r2 10', ins.Blth('r1', 'r2', 10))]

    def test_correct_result(self):
        """Test correct Result computed and fed by Decode stage."""
        for delay in [1, 2, 5, 10]:
            self.decode.DELAY = delay
            exp_log = []
            self.feed_log.log = []
            for (ins_str, exp_ins) in self.test_strs:
                self.decode.feed(ins_str)
                self.decode.tick() # Fed ins_str becomes current state.
                for _ in range(self.decode.DELAY):
                    # Check Instruction not output before DELAY ticks.
                    self.assertTrue(instruction_list_equal(self.feed_log.log,
                                                           exp_log))
                    self.decode.tick()
                exp_log.append(exp_ins)
                self.assertTrue(instruction_list_equal(self.feed_log.log,
                                                       exp_log))

    def test_busy(self):
        """Test IntegerUnit busy method updates correctly after ticks."""
        for delay in [1, 2, 5, 10]:
            self.decode.DELAY = delay
            for ins_str, _ in self.test_strs:
                self.assertFalse(self.decode.busy(),
                                 'Decode busy after initialization')
                self.decode.feed(ins_str)
                self.assertTrue(self.decode.busy(),
                                'Decode not busy after being fed')
                for _ in range(self.decode.DELAY - 1):
                    self.decode.tick()
                    self.assertTrue(self.decode.busy(),
                                    'Decode not busy before DELAY ticks')
                self.decode.tick()
                self.assertFalse(self.decode.busy(),
                                 'Decode busy after DELAY ticks')

    def test_decode_str(self):
        for ins_str, exp_ins in self.test_strs:
            self.assertTrue(instruction_list_equal([decode._decode(ins_str)],
                                                   [exp_ins]))
