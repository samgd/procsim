from procsim.back_end.result import Result
from procsim.instructions.memory_access import MemoryAccess
from procsim.memory import Memory

class Store(MemoryAccess):
    """Store instruction.

    Args:
        rs: Store Register name.
        r1: Source 1 Register name.
    """

    def __init__(self, rs, r1):
        super().__init__()
        self.rs = rs
        self.r1 = r1

    def execute(self, register_file, memory):
        dest = register_file[self.r1]
        value = register_file[self.rs]
        return Result(dest, value, Memory)

    def __repr__(self):
        return 'Store(%r, %r)' % (self.rs, self.r1)

    def __str__(self):
        return 'str %s %s' % (self.rs, self.r1)
