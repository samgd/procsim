import abc

class Instruction(abc.ABC):
    """Base class for all instructions.

    Attributes:
        DELAY: Default instruction-execution delay.
    """

    def __init__(self):
        self.DELAY = 1
