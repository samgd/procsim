from procsim.back_end.result import Result
from procsim.instructions import BranchJump

class Blth(BranchJump):
    """Branch less than instruction.

    Args:
        r1: Source 1 Register name.
        r2: Source 2 Register name.
        imm: Immediate address to branch to.
    """

    def __init__(self, r1, r2, imm):
        super().__init__()
        self.r1 = r1
        self.r2 = r2
        self.imm = imm

    def execute(self, register_file):
        """Execute Blth and return the Result, if any.

        Note: This does _not_ write to the RegisterFile.

        Args:
            register_file: A RegisterFile to read Register values from.

        Returns:
            The Result if r1 < r2 else None.
        """
        if register_file[self.r1] < register_file[self.r2]:
            return Result('pc', self.imm)

    def __repr__(self):
        return 'Blth(%r, %r, %r)' % (self.r1, self.r2, self.imm)

    def __str__(self):
        return 'blth %s %s %s' % (self.r1, self.r2, self.imm)
