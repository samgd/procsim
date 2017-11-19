from procsim.back_end.instructions.memory_access import MemoryAccess

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

    def execute(self, memory):
        raise NotImplementedError('TODO')
