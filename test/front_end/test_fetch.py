import os
import unittest

from procsim.front_end.fetch import Fetch
from procsim.register_file import RegisterFile
from test.feed_log import FeedLog
from test.front_end.utils import make_program_file
import procsim.instructions as ins

TEST_PROGRAM = [ins.Add('r1', 'r2', 'r3'),
                ins.AddI('r2', 'r2', 5),
                ins.SubI('r2', 'r2', 5),
                ins.Sub('r1', 'r2', 'r3')]

class TestFetch(unittest.TestCase):

    def setUp(self):
        # Create temporary, convert and write TEST_PROGRAM.
        self.program_file = make_program_file(TEST_PROGRAM)
        self.test_program_str = [str(i) for i in TEST_PROGRAM]

        # Initialize Fetch.
        self.reg_file = RegisterFile(10)
        self.feed_log = FeedLog()
        self.fetch = Fetch(self.reg_file,
                           self.program_file,
                           self.feed_log)

    def tearDown(self):
        os.remove(self.program_file)

    def test_operate(self):
        """Test Fetch feeds correct instruction strings."""
        for i in range(1, len(TEST_PROGRAM) + 1):
            self.fetch.tick()
            self.assertListEqual(self.feed_log.log,
                                 self.test_program_str[:i])
            self.assertEqual(self.reg_file['pc'], i)
