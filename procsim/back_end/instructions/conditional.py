from procsim.back_end.instructions.branch import Branch
from procsim.back_end.result import Result

class Conditional(Branch):
    """Conditional Branch Instruction.

    Args:
        tag: Tag to identify location inside ROB.
        operation: Binary conditional operation to apply to operand_1 and
            operand_2.
        operand_1, operand_2: Operands for condition operation.
    """

    def __init__(self, tag, operation, operand_1, operand_2):
        super().__init__()
        self.DELAY = 2
        self.tag = tag
        self.operation = operation
        self.operand_1 = operand_1
        self.operand_2 = operand_2

    def receive(self, result):
        if self.operand_1 == result.tag:
            self.operand_1 = result.value
        if self.operand_2 == result.tag:
            self.operand_2 = result.value

    def can_dispatch(self):
        return (isinstance(self.operand_1, int)
                and isinstance(self.operand_2, int))

    def execute(self):
        if not self.can_dispatch():
            raise ValueError('unable to execute: operand(s) not available')
        value = self.operation(self.operand_1, self.operand_2)
        return Result(self.tag, value, typ=Branch)
