from procsim.back_end.instructions.memory_access import MemoryAccess
from procsim.back_end.result import Result

class Store(MemoryAccess):
    """Store MemoryAccess Instruction.

    Args:
        tag: Tag to identify location inside ROB.
        address: Address in Memory to Store value to.
        value: Value to Store to Memory.
    """

    def __init__(self, address, value):
        super().__init__('Store', address)
        self.value = value

    def receive(self, result):
        super().receive(result)
        if self.value == result.tag:
            self.value = result.value

    def can_dispatch(self):
        return isinstance(self.address, int) and isinstance(self.value, int)

    def execute(self, memory):
        if not self.can_dispatch():
            raise ValueError('unable to execute: operand(s) not available')
        memory[self.address] = self.value
