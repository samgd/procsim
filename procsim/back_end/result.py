from procsim.register import Register

class Result:
    """Result of executing an Instruction.

    Args:
        tag: Tag to identify location inside ROB.
        value: Result of executing an instruction.
        typ: Result type. Specifies the type of the Result.
            (default Register)

    Attributes:
        tag: Tag to identify location inside ROB.
        value: Result of executing an instruction.
        typ: Result type. Specifies the type of the Result.
            (default Register)
    """

    def __init__(self, tag, value, typ=Register):
        self.tag = tag
        self.value = value
        self.typ = typ

    def __eq__(self, other):
        """Results are equal if they have equal tag and value attributes."""
        return type(other) is type(self) and self.__dict__ == other.__dict__

    def __repr__(self):
        return 'Result(%r, %r, %s)' % (self.tag, self.value, self.typ.__name__)
