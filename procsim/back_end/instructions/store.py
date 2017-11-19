from procsim.back_end.instructions.memory_access import MemoryAccess
from procsim.back_end.result import Result

class Store(MemoryAccess):
    """Store MemoryAccess Instruction.

    Args:
        tag: Tag to identify location inside ROB.
        address: Address in Memory to Store value to.
        value: Value to Store to Memory.
    """

    def __init__(self, tag, address, value):
        super().__init__(tag, address)
        self.value = value

    def receive(self, result):
        super().receive(result)
        if self.value == result.tag:
            self.value = result.value

    def execute(self):
        if not isinstance(self.address, int) or not isinstance(self.value, int):
            raise ValueError('unable to execute: operand(s) not available')
        return Result(self.tag, (self.address, self.value), typ=Store)
