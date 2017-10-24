from procsim.register import Register

class Result:
    """Result of executing an Instruction.

    Args:
        dest: Register or Memory address to write value in, depending on the
            Result typ.
        value: Value to write in dest.
        typ: Result type. Specifies the semantic meaning of dest.
            (default Register)

    Attributes:
        dest: Register or Memory address to write value in, depending on the
            Result typ.
        value: Value to write in dest.
        typ: Result type. Specifies the semantic meaning of dest.
            (default Register)
    """

    def __init__(self, dest, value, typ=Register):
        self.dest = dest
        self.value = value
        self.typ = typ

    def __eq__(self, other):
        """Results are equal if they have equal dest and value attributes."""
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __repr__(self):
        return 'Result(%r, %r, %s)' % (self.dest, self.value, self.typ.__name__)
