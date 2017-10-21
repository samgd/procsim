import abc

from procsim.instructions.instruction import Instruction

class BranchJump(Instruction):
    """Abstract class for branch or jump Instructions."""

    def __init__(self):
        super().__init__()
        self.DELAY = 1

    @abc.abstractmethod
    def execute(self, register_file):
        """Execute the BranchJump Instruction and return the Result."""
        pass
