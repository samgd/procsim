from procsim.back_end.instructions.memory_access import MemoryAccess

class Store(MemoryAccess):
    """Store MemoryAccess Instruction."""

    def __init__(self, tag, address, value):
        super().__init__(tag, address, value)

    def execute(self, memory):
        raise NotImplementedError('TODO')
