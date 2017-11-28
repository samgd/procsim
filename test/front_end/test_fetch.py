import math
import unittest

from procsim.branch.branch_info import BranchInfo
from procsim.branch.static.never_taken import NeverTaken
from procsim.front_end.fetch import Fetch
from procsim.front_end.instructions import Add
from procsim.front_end.instructions import AddI
from procsim.front_end.instructions import Blth
from procsim.front_end.instructions import Sub
from procsim.front_end.instructions import SubI
from procsim.register_file import RegisterFile
from test.feed_log import FeedLog
from test.flushable_log import FlushableLog

TEST_PROGRAM = [Add('r1', 'r2', 'r3'),
                AddI('r2', 'r2', 5),
                SubI('r2', 'r2', 5),
                Sub('r1', 'r2', 'r3')]

class TestFetch(unittest.TestCase):

    def setUp(self):
        self.reg_file = RegisterFile(10)
        self.feed_log = FeedLog()
        self.branch_predictor = NeverTaken()

    def test_operate(self):
        """Test Fetch feeds correct instruction strings."""
        test_program_str = [str(i) for i in TEST_PROGRAM]

        for width in [1, 2, 3]:
            self.feed_log.reset()
            self.reg_file['pc'] = 0

            fetch = Fetch(self.reg_file,
                          test_program_str,
                          self.feed_log,
                          self.branch_predictor,
                          width=width)

            n_inst = len(TEST_PROGRAM)
            n_fetch = 0
            while n_fetch <= n_inst:
                fetch.tick()
                n_fetch += width
                self.assertListEqual(self.feed_log.log,
                                     [{'instruction_str': ins_str}
                                      for ins_str in test_program_str[:n_fetch]])
                self.assertEqual(self.reg_file['pc'], min(n_fetch, n_inst))
            # PC is now beyond # program instructions. Tick ensures Fetch handles
            # this gracefully.
            fetch.tick()

    def test_conditional_branch_tag(self):
        ins = Blth('r1', 'r2', 10)
        ins_str = str(ins)

        fetch = Fetch(self.reg_file,
                      [ins_str],
                      self.feed_log,
                      self.branch_predictor)
        fetch.tick()

        exp_ins = {'instruction_str': ins_str,
                   'branch_info': BranchInfo(False, 10, 1, 0)}

        self.assertDictEqual(self.feed_log.log[0], exp_ins)

    def test_flush(self):
        """Ensure flush flushes Fetch and Decode."""
        log = FlushableLog()
        self.feed_log.flush = log.flush

        fetch = Fetch(self.reg_file,
                      [],
                      self.feed_log,
                      self.branch_predictor)
        fetch.flush()
        self.assertEqual(log.n_flush, 1, 'Fetch must flush Decode')

    def test_unconditional_branch_set_pc(self):
        """Ensure Fetch detects unconditional branch and sets pc."""
        self.reg_file['pc'] = 0
        fetch = Fetch(self.reg_file,
                      ['j 100'],
                      self.feed_log,
                      self.branch_predictor)
        fetch.tick()
        fetch.tick()
        self.assertEqual(self.reg_file['pc'], 100,
                         'Fetch should detect unconditional branches and set pc')
