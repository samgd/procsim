class BranchInfo:
    """Information about a conditional branch instruction.

    Attributes:
        taken: Bool - True if conditional branch was taken by the Fetch unit.
        taken_addr: Address of next instruction to fetch if the conditional
            branch instruction was to be taken.
        not_taken_addr: Address of next instruction to fetch if the conditional
            branch instruction was not to be taken.
    """

    def __init__(self, taken, taken_addr, not_taken_addr):
        self.taken = taken
        self.taken_addr = taken_addr
        self.not_taken_addr = not_taken_addr

    def __repr__(self):
        return '%s(%r, %r, %r)' % (type(self).__name__,
                                   self.taken,
                                   self.taken_addr,
                                   self.not_taken_addr)

    def __eq__(self, other):
        return (isinstance(self, other.__class__)
                and self.__dict__ == other.__dict__)
