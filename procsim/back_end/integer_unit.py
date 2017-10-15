from procsim.back_end.result import Result
from procsim.feedable import Feedable
from procsim.instructions import Add
from procsim.tickable import Tickable

class IntegerUnit(Tickable, Feedable):
    """A single integer execution unit capable of integer and logical ops.

    The execution delay is taken from the Instruction's DELAY attribute.

    Args:
        register_file: RegisterFile to read Register values from when executing
            operations.
        write_unit: WriteUnit to pass execution Result to.
    """

    def __init__(self, register_file, write_unit):
        self.reg_file = register_file
        self.write_unit = write_unit
        self.inst = None
        self.compute_timer = 0

    def feed(self, instruction):
        """Feed the IntegerUnit an Instruction to execute.

        Args:
            instruction: An IntegerLogical Instruction to execute.
        """
        assert self.inst is None, 'IntegerUnit fed when busy'
        self.inst = instruction
        self.compute_timer = instruction.DELAY

    def busy(self):
        """Return True if the IntegerUnit is busy.

        The unit can be busy when either executing an Instruction or waiting
        for the WriteUnit to become free.
        """
        return self.inst is not None

    def tick(self):
        """(Continue to) Execute the Instruction and write Result if possible."""
        self.compute_timer = max(0, self.compute_timer - 1)
        if self.inst and self.compute_timer == 0 and not self.write_unit.busy():
            result = self.inst.execute(self.reg_file)
            self.write_unit.feed(result)
            self.inst = None
