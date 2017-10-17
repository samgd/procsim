from procsim.instructions.memory_access import MemoryAccess

class Store(MemoryAccess):
    """Store instruction.

    Args:
        rs: Store Register name.
        r1: Source 1 Register name.
    """

    def __init__(self, rs, r1):
        super.__init__()
        self.rs = rs
        self.r1 = r1

    def __repr__(self):
        return 'Store(%r, %r)' % (self.rs, self.r1)

    def execute(self, register_file, memory):
        pass
