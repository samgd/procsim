from procsim.back_end.instructions.memory_access import MemoryAccess
from procsim.back_end.result import Result

class Load(MemoryAccess):
    """Load MemoryAccess Instruction.

    Args:
        tag: Tag to identify location inside ROB.
        address: Address in Memory to Load a value from.
    """

    def __init__(self, tag, address):
        super().__init__(tag, address)

    def receive(self, result):
        super().receive(result)

    def execute(self, memory):
        if not self.can_execute():
            raise ValueError('unable to execute: operand(s) not available')
        return Result(self.tag, memory[self.address])

    def can_execute(self):
        return self.can_dispatch()
