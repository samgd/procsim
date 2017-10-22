from copy import deepcopy
import os
import unittest

from procsim.front_end.decode import Decode
from procsim.front_end.fetch import Fetch
from procsim.register_file import RegisterFile
from test.feed_log import FeedLog
from test.front_end.utils import make_program_file
import procsim.instructions as ins

TEST_PROGRAM = [ins.Add('r1', 'r2', 'r3'),
                ins.AddI('r2', 'r2', 5),
                ins.SubI('r2', 'r2', 5),
                ins.Sub('r1', 'r2', 'r3')]

class TestFetchDecodeIntegration(unittest.TestCase):

    def init_run(self):
        self.program_file = make_program_file(TEST_PROGRAM)

        self.feed_log = FeedLog()
        self.decode = Decode(self.feed_log)

        self.reg_file = RegisterFile(10)
        self.fetch = Fetch(self.reg_file,
                           self.program_file,
                           self.decode)

    def cleanup_run(self):
        os.remove(self.program_file)

    def test_fetch_decode_integration(self):
        """Ensure different operate and trigger both produce the TEST_PROGRAM."""

        for run in range(2):
            self.init_run()

            for _ in range(15):
                if run == 'run_0':
                    self.decode.operate()
                    self.fetch.operate()
                    self.decode.trigger()
                    self.fetch.trigger()
                else:
                    self.fetch.operate()
                    self.decode.operate()
                    self.fetch.trigger()
                    self.decode.trigger()

            self.assertEqual(self.feed_log.log, TEST_PROGRAM)
            self.cleanup_run()
