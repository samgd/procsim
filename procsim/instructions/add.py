from procsim.back_end.result import Result
from procsim.instructions.integer_logical import IntegerLogical

class Add(IntegerLogical):
    """Add register instruction.

    Args:
        rd: Destination Register name.
        r1: Source 1 Register name.
        r2: Source 2 Register name.
    """

    def __init__(self, rd, r1, r2):
        super().__init__()
        self.rd = rd
        self.r1 = r1
        self.r2 = r2

    def execute(self, register_file):
        """Execute add and return the Result.

        Note: This does _not_ write to the Result to the RegisterFile.

        Args:
            register_file: A RegisterFile to read Register values from.

        Returns:
            The Result.
        """
        return Result(self.rd, register_file[self.r1] + register_file[self.r2])

    def __repr__(self):
        return 'Add(%r, %r, %r)' % (self.rd, self.r1, self.r2)

    def __str__(self):
        return 'add %s %s %s' % (self.rd, self.r1, self.r2)
