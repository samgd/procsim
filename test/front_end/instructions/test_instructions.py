import unittest

import procsim.front_end.instructions as ins

class TestInstructions(unittest.TestCase):
    """Test Instruction repr and str to catch any superficial display bugs."""

    def test_add_display(self):
        args = ('R0', 'R1', 'R2')
        add = ins.Add(*args)
        self.assertEqual(repr(add), "Add('R0', 'R1', 'R2')")
        self.assertEqual(str(add), 'add R0 R1 R2')

    def test_addi_display(self):
        args = ('R0', 'R1', 10)
        addi = ins.AddI(*args)
        self.assertEqual(repr(addi), "AddI('R0', 'R1', 10)")
        self.assertEqual(str(addi), 'addi R0 R1 10')

    def test_sub_display(self):
        args = ('R0', 'R1', 'R2')
        sub = ins.Sub(*args)
        self.assertEqual(repr(sub), "Sub('R0', 'R1', 'R2')")
        self.assertEqual(str(sub), 'sub R0 R1 R2')

    def test_subi_display(self):
        args = ('R0', 'R1', 10)
        subi = ins.SubI(*args)
        self.assertEqual(repr(subi), "SubI('R0', 'R1', 10)")
        self.assertEqual(str(subi), 'subi R0 R1 10')

    def test_mul_display(self):
        args = ('R0', 'R1', 'R2')
        mul = ins.Mul(*args)
        self.assertEqual(repr(mul), "Mul('R0', 'R1', 'R2')")
        self.assertEqual(str(mul), 'mul R0 R1 R2')

    def test_muli_display(self):
        args = ('R0', 'R1', 10)
        muli = ins.MulI(*args)
        self.assertEqual(repr(muli), "MulI('R0', 'R1', 10)")
        self.assertEqual(str(muli), 'muli R0 R1 10')

    def test_load_display(self):
        args = ('r0', 'r1')
        load = ins.Load(*args)
        self.assertEqual(repr(load), "Load('r0', 'r1')")
        self.assertEqual(str(load), 'ldr r0 r1')

    def test_store_display(self):
        args = ('y1', 'y10')
        store = ins.Store(*args)
        self.assertEqual(repr(store), "Store('y1', 'y10')")
        self.assertEqual(str(store), 'str y1 y10')

    def test_jump_display(self):
        args = (55,)
        jump = ins.Jump(*args)
        self.assertEqual(repr(jump), "Jump(55)")
        self.assertEqual(str(jump), 'j 55')

    def test_blth_display(self):
        args = ('x0', 'x10', 99)
        blth = ins.Blth(*args)
        self.assertEqual(repr(blth), "Blth('x0', 'x10', 99)")
        self.assertEqual(str(blth), 'blth x0 x10 99')

    def test_equality(self):
        ins1 = ins.Add('r1', 'r2', 'r3')
        ins2 = ins.Add('r1', 'r2', 'r3')
        ins3 = ins.Jump(100)
        self.assertFalse(ins1 == ins2)
        self.assertFalse(ins1 is ins2)
        self.assertFalse(ins2 == ins3)
