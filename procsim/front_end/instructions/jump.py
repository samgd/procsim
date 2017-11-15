class Jump:
    """Jump instruction.

    Args:
        imm: Immediate address to Jump to.
    """

    def __init__(self, imm):
        self.imm = imm

    def __repr__(self):
        return 'Jump(%r)' % self.imm

    def __str__(self):
        return 'j %s' % self.imm
