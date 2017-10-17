from procsim.instructions.memory_access import MemoryAccess

class Load(MemoryAccess):
    """Load instruction.

    Args:
        rd: Destination Register name.
        r1: Source 1 Register name.
    """

    def __init__(self, rd, r1):
        super.__init__()
        self.rd = rd
        self.r1 = r1

    def __repr__(self):
        return 'Load(%r, %r)' % (self.rd, self.r1)

    def execute(self, register_file, memory):
        pass
