from procsim.back_end.instructions.branch import Branch
from procsim.back_end.result import Result

class Unconditional(Branch):
    """Unconditional Branch Instruction.

    Args:
        tag: Tag to identify location inside ROB.
        operand: Address to Branch to.
    """

    def __init__(self, tag, operand):
        super().__init__()
        self.DELAY = 1
        self.tag = tag
        self.operand = operand

    def receive(self, result):
        if self.operand == result.tag:
            self.operand = result.value

    def can_dispatch(self):
        return isinstance(self.operand, int)

    def execute(self):
        if not self.can_dispatch():
            raise ValueError('unable to execute: operand not available')
        return Result(self.tag, self.operand, typ=Branch)
