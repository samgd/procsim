import os
import unittest

from test.front_end import utils
import procsim.instructions as ins

class TestUtils(unittest.TestCase):

    def test_make_program_file(self):
        instructions = [ins.Add('r0', 'r1', 'r2'),
                        ins.SubI('r2', 'r10', 100),
                        ins.Jump(0)]
        program_file = utils.make_program_file(instructions)
        with open(program_file, 'r') as prog:
            data = prog.read().split('\n')
            self.assertEqual(data, [str(i) for i in instructions])
        os.remove(program_file)
