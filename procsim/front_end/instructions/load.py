class Load:
    """Load instruction.

    Args:
        rd: Destination Register name.
        r1: Source 1 Register name.
    """

    def __init__(self, rd, r1):
        self.rd = rd
        self.r1 = r1

    def __repr__(self):
        return 'Load(%r, %r)' % (self.rd, self.r1)

    def __str__(self):
        return 'ldr %s %s' % (self.rd, self.r1)
