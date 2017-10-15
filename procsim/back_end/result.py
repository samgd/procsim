class Result:
    """Result of executing an Instruction.

    Args:
        dest: Name of Register to write value in.
        value: Value to write in dest.
    """

    def __init__(self, dest, value):
        self.dest = dest
        self.value = value
