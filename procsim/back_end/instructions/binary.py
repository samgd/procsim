from procsim.back_end.instructions.instruction import Instruction
from procsim.back_end.result import Result

class Binary(Instruction):
    """Binary Instruction that applies an operation to two operands.

    Args:
        tag: Tag to identify location inside ROB.
        operation: Binary operation to apply to operand_1 and operand_2.
        operand_1, operand_2: Operands for operation.
    """

    def __init__(self, tag, operation, operand_1, operand_2):
        super().__init__()
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
        return isinstance(self.operand_1, int) and isinstance(self.operand_2, int)

    def execute(self):
        if not self.can_dispatch():
            raise ValueError('unable to execute: operand(s) not available')
        return Result(self.tag, self.operation(self.operand_1, self.operand_2))
