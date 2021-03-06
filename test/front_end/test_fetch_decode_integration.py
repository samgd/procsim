from copy import deepcopy
import unittest

from procsim.branch.static.never_taken import NeverTaken
from procsim.front_end.decode import Decode
from procsim.front_end.fetch import Fetch
from procsim.front_end.instructions import Add
from procsim.front_end.instructions import AddI
from procsim.front_end.instructions import Sub
from procsim.front_end.instructions import SubI
from procsim.register_file import RegisterFile
from test.feed_log import FeedLog
from test.front_end.utils import instruction_list_equal

TEST_PROGRAM = [Add('r1', 'r2', 'r3'),
                AddI('r2', 'r2', 5),
                SubI('r2', 'r2', 5),
                Sub('r1', 'r2', 'r3')]

class TestFetchDecodeIntegration(unittest.TestCase):

    def init_run(self):
        self.test_program_str = [str(i) for i in TEST_PROGRAM]

        self.feed_log = FeedLog()
        self.feed_log.full = lambda _: False
        self.decode = Decode(self.feed_log)

        self.reg_file = RegisterFile(10)
        self.fetch = Fetch(self.reg_file,
                           self.test_program_str,
                           self.decode,
                           NeverTaken())

    def test_fetch_decode_integration(self):
        """Ensure different operate and trigger both produce the TEST_PROGRAM."""

        for run in range(2):
            self.init_run()

            for _ in range(15):
                if run == 0:
                    self.decode.operate()
                    self.fetch.operate()
                    self.decode.trigger()
                    self.fetch.trigger()
                else:
                    self.fetch.operate()
                    self.decode.operate()
                    self.fetch.trigger()
                    self.decode.trigger()

            self.assertTrue(instruction_list_equal(self.feed_log.log,
                                                   TEST_PROGRAM))
