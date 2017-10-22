from procsim.back_end.result import Result
from procsim.instructions import BranchJump

class Jump(BranchJump):
    """Jump instruction.

    Args:
        imm: Immediate address to Jump to.
    """

    def __init__(self, imm):
        super().__init__()
        self.imm = imm

    def execute(self, register_file):
        """Execute Jump and return the Result.

        Note: This does _not_ write to the RegisterFile.

        Args:
            register_file: A RegisterFile to read Register values from.

        Returns:
            The Result.
        """
        return Result('pc', self.imm)

    def __repr__(self):
        return 'Jump(%r)' % self.imm

    def __str__(self):
        return 'j %s' % self.imm
