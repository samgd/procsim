class Store:
    """Store instruction.

    Args:
        rs: Name of register to store.
        r1: Name of register holding Memory.
    """

    def __init__(self, rs, r1):
        self.rs = rs
        self.r1 = r1

    def __repr__(self):
        return 'Store(%r, %r)' % (self.rs, self.r1)

    def __str__(self):
        return 'str %s %s' % (self.rs, self.r1)
