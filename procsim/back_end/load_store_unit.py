from procsim.back_end.execution_unit import ExecutionUnit
from procsim.instructions import MemoryAccess

class LoadStoreUnit(ExecutionUnit):
    """A single LoadStoreUnit capable of performing memory access operations.

    The execution delay is taken from the Instruction's DELAY attribute.

    Args:
        register_file: RegisterFile to read Register values from when executing
            operations.
        write_unit: WriteUnit to pass execution Result to.
        memory: Memory to address when executing operations.
    """

    def __init__(self, register_file, write_unit, memory):
        super().__init__()
        self.register_file = register_file
        self.write_unit = write_unit
        self.memory = memory

    def feed(self, instruction):
        ...

    def busy(self):
        ...

    def operate(self):
        ...

    def trigger(self):
        ...

    def capability(self):
        return MemoryAccess
