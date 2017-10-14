import unittest

import procsim.instructions as ins

class TestInstructions(unittest.TestCase):

    # Test repr to catch any obvious init and repr bugs.
    def test_add_repr(self):
        args = ('R0', 'R1', 'R2')
        add = ins.Add(*args)
        self.assertEqual(repr(add), "Add(%r, %r, %r)" % args)

    def test_addi_repr(self):
        args = ('R0', 'R1', 10)
        addi = ins.AddI(*args)
        self.assertEqual(repr(addi), "AddI(%r, %r, %r)" % args)

    def test_sub_repr(self):
        args = ('R0', 'R1', 'R2')
        sub = ins.Sub(*args)
        self.assertEqual(repr(sub), "Sub(%r, %r, %r)" % args)

    def test_subi_repr(self):
        args = ('R0', 'R1', 10)
        subi = ins.SubI(*args)
        self.assertEqual(repr(subi), "SubI(%r, %r, %r)" % args)

    def test_load_repr(self):
        args = ('r0', 'r1')
        load = ins.Load(*args)
        self.assertEqual(repr(load), "Load(%r, %r)" % args)

    def test_store_repr(self):
        args = ('y1', 'y10')
        store = ins.Store(*args)
        self.assertEqual(repr(store), "Store(%r, %r)" % args)

    def test_jump_repr(self):
        args = (55,)
        jump = ins.Jump(*args)
        self.assertEqual(repr(jump), "Jump(%r)" % args)

    def test_blth_repr(self):
        args = ('x0', 'x10', 99)
        blth = ins.Blth(*args)
        self.assertEqual(repr(blth), "Blth(%r, %r, %r)" % args)
