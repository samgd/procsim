from procsim.back_end.instructions.binary import Binary

class IntegerLogical(Binary):
    """Binary integer and logical Instructions."""

    def __init__(self, tag, operation, operand_1, operand_2):
        super().__init__(tag, operation, operand_1, operand_2)
        self.DELAY = 2
