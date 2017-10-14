class Store:
    """Store instruction.

    Args:
        rs: Store Register name.
        r1: Source 1 Register name.
    """

    def __init__(self, rs, r1):
        self.rs = rs
        self.r1 = r1

    def __repr__(self):
        return 'Store(%r, %r)' % (self.rs, self.r1)
