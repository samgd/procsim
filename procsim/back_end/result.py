class Result:
    """Result of executing an Instruction.

    Args:
        dest: Name of Register to write value in.
        value: Value to write in dest.

    Attributes:
        dest: Name of Register to write value in.
        value: Value to write in dest.
    """

    def __init__(self, dest, value):
        self.dest = dest
        self.value = value

    def __eq__(self, other):
        """Results are equal if they have equal dest and value attributes."""
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __repr__(self):
        return 'Result(%r, %r)' % (self.dest, self.value)
