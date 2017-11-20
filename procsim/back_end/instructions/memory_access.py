import abc

from procsim.back_end.instructions.instruction import Instruction

class MemoryAccess(Instruction):
    """MemoryAccess Instructions that Store or Load a value.

    Args:
        tag: Tag to identify location inside ROB.
        address: Address in Memory to Store or Load a value to or from.
        value: Value to Store or Load to Memory.
    """

    def __init__(self, tag, address):
        super().__init__()
        self.DELAY = 4
        self.tag = tag
        self.address = address

    def receive(self, result):
        if self.address == result.tag:
            self.address = result.value

    def can_dispatch(self):
        return isinstance(self.address, int)
