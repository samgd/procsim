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
        return self.dest == other.dest and self.value == other.value
