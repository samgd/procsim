import unittest

from procsim.front_end.fetch import Fetch
from procsim.front_end.instructions import Add
from procsim.front_end.instructions import AddI
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
        self.test_program_str = [str(i) for i in TEST_PROGRAM]

        # Initialize Fetch.
        self.reg_file = RegisterFile(10)
        self.feed_log = FeedLog()
        self.fetch = Fetch(self.reg_file,
                           self.test_program_str,
                           self.feed_log)

    def test_operate(self):
        """Test Fetch feeds correct instruction strings."""
        for i in range(1, len(TEST_PROGRAM) + 1):
            self.fetch.tick()
            self.assertListEqual(self.feed_log.log,
                                 self.test_program_str[:i])
            self.assertEqual(self.reg_file['pc'], i)
        # PC is now beyond # program instructions. Tick ensures Fetch handles
        # this gracefully.
        self.fetch.tick()
