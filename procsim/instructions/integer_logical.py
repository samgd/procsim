import abc

from procsim.instructions.instruction import Instruction

class IntegerLogical(Instruction):
    """Abstract class for integer and logical Instructions."""

    @abc.abstractmethod
    def execute(self, register_file):
        """Execute the integer or logical Instruction and return the Result."""
        pass
