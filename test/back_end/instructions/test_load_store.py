import unittest

from procsim.back_end.instructions.load import Load
from procsim.back_end.instructions.store import Store
from procsim.back_end.result import Result
from procsim.memory import Memory

class TestLoadStore(unittest.TestCase):

    def test_receive_and_can_dispatch_execute(self):
        for op in [Load, Store]:
            args = ('ROB1', 'ROB2')
            if op == Store:
                args += ('ROB3',)
            ins = op(*args)
            self.assertFalse(ins.can_dispatch())
            self.assertFalse(ins.can_execute())

            ins.receive(Result('ROB4', 0))
            self.assertFalse(ins.can_dispatch())
            self.assertFalse(ins.can_execute())

            ins.receive(Result('ROB1', 0))
            self.assertFalse(ins.can_dispatch())
            self.assertFalse(ins.can_execute())

            ins.receive(Result('ROB2', 7))
            self.assertEqual(ins.address, 7)
            self.assertTrue(ins.can_dispatch())
            if op == Load:
                self.assertTrue(ins.can_execute())

            if op == Store:
                ins.receive(Result('ROB3', 0))
                self.assertEqual(ins.value, 0)
                self.assertTrue(ins.can_dispatch())
                self.assertTrue(ins.can_execute())

    def test_load_execute(self):
        memory = Memory(64)
        memory[10] = 5
        load = Load('ROB1', 'ROB2')
        with self.assertRaises(ValueError):
            load.execute(memory)
        load.receive(Result('ROB2', 10))
        self.assertEqual(load.execute(memory), Result('ROB1', 5))

    def test_store_execute(self):
        store = Store('ROB2', 'ROB3', 'ROB4')
        for result in [Result('ROB3', 5), Result('ROB4', 10)]:
            with self.assertRaises(ValueError):
                store.execute()
            store.receive(result)
        self.assertEqual(store.execute(), Result('ROB2', (5, 10), typ=Store))

