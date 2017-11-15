class Mul:
    """Multiply Register instruction.

    Args:
        rd: Destination Register name.
        r1: Source 1 Register name.
        r2: Source 2 Register name.
    """

    def __init__(self, rd, r1, r2):
        self.rd = rd
        self.r1 = r1
        self.r2 = r2

    def __repr__(self):
        return 'Mul(%r, %r, %r)' % (self.rd, self.r1, self.r2)

    def __str__(self):
        return 'mul %s %s %s' % (self.rd, self.r1, self.r2)
