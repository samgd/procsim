from procsim.back_end.instructions.memory_access import MemoryAccess
from procsim.back_end.result import Result

class Load(MemoryAccess):
    """Load MemoryAccess Instruction.

    Args:
        tag: Tag to identify location inside ROB.
        address: Address in Memory to Load a value from.
    """

    def __init__(self, tag, address, uid=None, spec_exec=None):
        super().__init__(tag, address, uid, spec_exec)

    def receive(self, result):
        super().receive(result)

    def execute(self, memory):
        if not self.can_dispatch():
            raise ValueError('unable to execute: operand(s) not available')
        return Result(self.tag, memory[self.address])
