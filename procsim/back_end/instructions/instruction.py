import abc

class Instruction(abc.ABC):
    """Base class for all instructions.

    Attributes:
        DELAY: Default instruction-execution delay.
    """

    def __init__(self):
        self.DELAY = 1

    @abc.abstractmethod
    def receive(self, result):
        """Replace operand with result value if operand and result tags match.

        Args:
            result: The result of executing an Instruction.
        """
        pass

    @abc.abstractmethod
    def can_dispatch(self):
        """Return True if the Instruction is ready to be dispatched."""
        pass

    @abc.abstractmethod
    def execute(self):
        """Execute the Instruction."""
        pass
