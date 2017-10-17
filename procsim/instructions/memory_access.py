import abc

from procsim.instructions.instruction import Instruction

class MemoryAccess(Instruction):
    """Abstract class for MemoryAccess Instructions."""

    def __init__(self):
        super().__init__()
        self.DELAY = 4

    @abc.abstractmethod
    def execute(self, register_file, memory):
        """Execute the MemoryAccess Instruction and return the Result."""
        pass
