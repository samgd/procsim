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
        raise NotImplementedError('TODO')

    def __repr__(self):
        return 'Jump(%r)' % self.imm
