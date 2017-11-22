from procsim.back_end.execution_unit import ExecutionUnit
from procsim.back_end.instructions.integer_logical import IntegerLogical

class IntegerUnit(ExecutionUnit):
    """A single integer ExecutionUnit capable of integer and logical ops.

    The execution delay is taken from the Instruction's DELAY attribute.

    Args:
        broadcast_bus: BroadcastBus to publish Results to.
    """

    def __init__(self, broadcast_bus):
        super().__init__()
        self.broadcast_bus = broadcast_bus
        self.current_inst = None
        self.current_timer = 0
        self.future_inst = None
        self.future_timer = 0

    def feed(self, instruction):
        """Feed the IntegerUnit an Instruction to execute.

        Args:
            instruction: An IntegerLogical Instruction to execute.
        """
        assert self.future_inst is None, 'IntegerUnit fed when full'
        self.future_inst = instruction
        self.future_timer = max(0, instruction.DELAY - 1)

    def full(self):
        """Return True if the IntegerUnit's future state is non-empty."""
        return self.future_inst is not None

    def operate(self):
        """Publish Result to the BroadcastBus."""
        if self.current_inst and self.current_timer == 0:
            self.broadcast_bus.publish(self.current_inst.execute())
            if self.future_inst is self.current_inst:
                self.future_inst = None

    def trigger(self):
        """Advance the state of the IntegerUnit and init a new future state."""
        # Update current state.
        self.current_inst = self.future_inst
        self.current_timer = self.future_timer
        # Initialize future state.
        if self.current_inst is None:
            self.future_inst = None
            self.future_timer = 0
        else:
            self.future_inst = self.current_inst
            self.future_timer = max(0, self.current_timer - 1)

    def capability(self):
        return IntegerLogical

    def flush(self):
        self.current_inst = None
        self.current_timer = 0
        self.future_inst = None
        self.future_timer = 0
