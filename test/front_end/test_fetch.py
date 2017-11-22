import unittest

from procsim.front_end.branch_info import BranchInfo
from procsim.front_end.fetch import Fetch
from procsim.front_end.instructions import Add
from procsim.front_end.instructions import AddI
from procsim.front_end.instructions import Blth
from procsim.front_end.instructions import Sub
from procsim.front_end.instructions import SubI
from procsim.register_file import RegisterFile
from test.feed_log import FeedLog

TEST_PROGRAM = [Add('r1', 'r2', 'r3'),
                AddI('r2', 'r2', 5),
                SubI('r2', 'r2', 5),
                Sub('r1', 'r2', 'r3')]

class TestFetch(unittest.TestCase):

    def setUp(self):
        self.reg_file = RegisterFile(10)
        self.feed_log = FeedLog()

    def test_operate(self):
        """Test Fetch feeds correct instruction strings."""
        test_program_str = [str(i) for i in TEST_PROGRAM]

        fetch = Fetch(self.reg_file,
                      test_program_str,
                      self.feed_log)

        for i in range(1, len(TEST_PROGRAM) + 1):
            fetch.tick()
            self.assertListEqual(self.feed_log.log,
                                 [{'instruction_str': ins_str}
                                  for ins_str in test_program_str[:i]])
            self.assertEqual(self.reg_file['pc'], i)
        # PC is now beyond # program instructions. Tick ensures Fetch handles
        # this gracefully.
        fetch.tick()

    def test_conditional_branch_tag(self):
        ins = Blth('r1', 'r2', 10)
        ins_str = str(ins)

        fetch = Fetch(self.reg_file, [ins_str], self.feed_log)
        fetch.tick()

        exp_ins = {'instruction_str': ins_str,
                   'branch_info': BranchInfo(False, 10, 1)}

        self.assertDictEqual(self.feed_log.log[0], exp_ins)
