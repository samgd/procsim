import unittest

import procsim.instructions as ins
from procsim.front_end import decode

class TestDecode(unittest.TestCase):

    def setUp(self):
        self.rs = ''

    def test_decode_str(self):
        tests = [('add r1 r2 r3', ins.Add('r1', 'r2', 'r3')),
                 ('addi r1 r2 5', ins.AddI('r1', 'r2', 5)),
                 ('sub rd r0 r9', ins.Sub('rd', 'r0', 'r9')),
                 ('subi r1 r2 10', ins.SubI('r1', 'r2', 10)),
                 ('ldr r0 r1', ins.Load('r0', 'r1')),
                 ('str r99 r100', ins.Store('r99', 'r100')),
                 ('j 1000', ins.Jump(1000)),
                 ('blth r1 r2 10', ins.Blth('r1', 'r2', 10))]
        for ins_str, exp_ins in tests:
            self.assertEqual(decode._decode(ins_str), exp_ins)
