import unittest

from procsim.back_end.instructions.load import Load
from procsim.back_end.instructions.store import Store
from procsim.back_end.result import Result
from procsim.memory import Memory

class TestLoadStore(unittest.TestCase):

    def test_load_receive_and_can_dispatch_execute(self):
        ins = Load('ROB1', 'ROB2')
        self.assertFalse(ins.can_dispatch())

        ins.receive(Result('ROB4', 0))
        self.assertFalse(ins.can_dispatch())

        ins.receive(Result('ROB1', 0))
        self.assertFalse(ins.can_dispatch())

        ins.receive(Result('ROB2', 7))
        self.assertEqual(ins.address, 7)
        self.assertTrue(ins.can_dispatch())

    def test_store_receive_and_can_dispatch_execute(self):
        ins = Store('ROB7', 'ROB8')
        self.assertFalse(ins.can_dispatch())

        ins.receive(Result('ROB4', 0))
        self.assertFalse(ins.can_dispatch())

        ins.receive(Result('ROB7', 0))
        self.assertEqual(ins.address, 0)
        self.assertFalse(ins.can_dispatch())

        ins.receive(Result('ROB8', 7))
        self.assertTrue(ins.can_dispatch())

    def test_load_execute(self):
        memory = Memory(64)
        memory[10] = 5
        load = Load('ROB1', 'ROB2')
        with self.assertRaises(ValueError):
            load.execute(memory)
        load.receive(Result('ROB2', 10))
        self.assertEqual(load.execute(memory), Result('ROB1', 5))

    def test_store_execute(self):
        memory = Memory(64)
        memory[10] = 0
        store = Store('ROB3', 'ROB4')
        for result in [Result('ROB3', 10), Result('ROB4', 5)]:
            with self.assertRaises(ValueError):
                store.execute(memory)
            store.receive(result)
        store.execute(memory)
        self.assertEqual(memory[10], 5)

