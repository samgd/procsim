from procsim.back_end.instructions.branch import Branch
from procsim.back_end.instructions.binary import Binary

class Conditional(Binary, Branch):
    """Conditional Branch Instruction."""

    def __init__(self, tag, operation, operand_1, operand_2):
        super().__init__(tag, operation, operand_1, operand_2)
        self.DELAY = 2
