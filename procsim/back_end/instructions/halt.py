from procsim.back_end.instructions.instruction import Instruction

class Halt(Instruction):
    """Halt Instruction."""

    def __init__(self, tag):
        super().__init__()
        self.tag = tag

    def receive(self, result):
        pass

    def can_dispatch(self):
        return True

    def execute(self):
        pass
