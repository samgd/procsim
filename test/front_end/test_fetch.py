import locale
import os
import tempfile
import unittest

from procsim.front_end.fetch import Fetch
from procsim.register_file import RegisterFile
from test.front_end.decode_stub import DecodeStub
import procsim.instructions as ins

TEST_PROGRAM = [ins.Add('r1', 'r2', 'r3'),
                ins.AddI('r2', 'r2', 5),
                ins.SubI('r2', 'r2', 5),
                ins.Sub('r1', 'r2', 'r3')]

class TestFetch(unittest.TestCase):

    def setUp(self):
        """Create a temporary program file and Fetch stage."""
        # Create temporary, convert and write TEST_PROGRAM.
        (program, self.program_file) = tempfile.mkstemp()
        encoding = locale.getpreferredencoding(False)
        self.test_program_str = [str(i) for i in TEST_PROGRAM]
        data = b'\n'.join([bytearray(ins_str, encoding)
                           for ins_str in self.test_program_str])
        os.write(program, data)
        os.close(program)

        # Initialize Fetch.
        self.reg_file = RegisterFile(10)
        self.decode_stub = DecodeStub()
        self.fetch = Fetch(self.reg_file,
                           self.program_file,
                           self.decode_stub)

    def tearDown(self):
        """Remove temporary program file."""
        os.remove(self.program_file)

    def test_operate(self):
        """Test Fetch passes DecodeStub correct instruction strings."""
        for i in range(1, len(TEST_PROGRAM) + 1):
            self.fetch.tick()
            self.assertListEqual(self.decode_stub.log,
                                 self.test_program_str[:i])
            self.assertEqual(self.reg_file['pc'], i)
