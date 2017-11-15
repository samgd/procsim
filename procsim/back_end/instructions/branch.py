from procsim.back_end.instructions.instruction import Instruction

class Branch(Instruction):
    """Abstract class for Branch Instructions."""

    def __init__(self):
        super().__init__()
