from procsim.instructions import BranchJump

class Blth(BranchJump):
    """Branch less than instruction.

    Args:
        r1: Source 1 Register name.
        r2: Source 2 Register name.
        imm: Immediate address to branch to.
    """

    def __init__(self, r1, r2, imm):
        self.r1 = r1
        self.r2 = r2
        self.imm = imm

    def execute(self, register_file):
        raise NotImplementedError('TODO')

    def __repr__(self):
        return 'Blth(%r, %r, %r)' % (self.r1, self.r2, self.imm)

    def __str__(self):
        return 'blth %s %s %s' % (self.r1, self.r2, self.imm)
