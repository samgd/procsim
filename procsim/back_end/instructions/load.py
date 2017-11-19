from procsim.back_end.instructions.memory_access import MemoryAccess

class Load(MemoryAccess):
    """Load MemoryAccess Instruction.

    Args:
        tag: Tag to identify location inside ROB.
        address: Address in Memory to Load a value from.
    """

    def __init__(self, tag, address):
        super().__init__(tag, address)
        self.value = None

    def receive(self, result):
        super().receive(result)

    def execute(self, memory):
        raise NotImplementedError('TODO')
