class MulI:
    """Multiply immediate instruction.

    Args:
        rd: Destination Register name.
        r1: Source 1 Register name.
        imm: Immediate value.
    """

    def __init__(self, rd, r1, imm):
        self.rd = rd
        self.r1 = r1
        self.imm = imm

    def __repr__(self):
        return 'MulI(%r, %r, %r)' % (self.rd, self.r1, self.imm)

    def __str__(self):
        return 'muli %s %s %s' % (self.rd, self.r1, self.imm)
