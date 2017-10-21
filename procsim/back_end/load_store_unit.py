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
        self.reg_file = register_file
        self.write_unit = write_unit
        self.memory = memory
        self.current_inst = None
        self.current_timer = 0
        self.future_inst = None
        self.future_timer = 0

    def feed(self, instruction):
        """Feed the LoadStoreUnit an Instruction to execute)

        Args:
            instruction: A MemoryAccess Instruction to execute.
        """
        assert self.future_inst is None, 'LoadStoreUnit fed when busy'
        self.future_inst = instruction
        self.future_timer = max(0, instruction.DELAY - 1)

    def busy(self):
        """Return True if the LoadStoreUnit's future state is non-empty."""
        return self.future_inst is not None

    def operate(self):
        """Feed Result to the WriteUnit if possible."""
        if self.current_inst and self.current_timer == 0 and not self.write_unit.busy():
            self.write_unit.feed(self.current_inst.execute(self.reg_file, self.memory))

    def trigger(self):
        """Advance the state of the LoadStoreUnit and init a new future state."""
        # Update current state.
        self.current_inst = self.future_inst
        self.current_timer = self.future_timer
        # Initialize future state.
        if self.current_inst is None or self.current_timer == 0:
            self.future_inst = None
            self.future_timer = 0
        else:
            self.future_inst = self.current_inst
            self.future_timer = max(0, self.current_timer - 1)

    def capability(self):
        return MemoryAccess
