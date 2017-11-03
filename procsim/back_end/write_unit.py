from procsim.back_end.execution_unit import ExecutionUnit
from procsim.back_end.result import Result
from procsim.memory import Memory
from procsim.register import Register

class WriteUnit(ExecutionUnit):
    """A WriteUnit writes Results to a RegisterFile after a number of ticks.

    Args:
        register_file: RegisterFile to write Register Result values to.
        memory: Memory to write Memory Result values to.
        write_delay: Number of trigger calls to wait before writing a Result to
            the register_file. (default 1)
    """

    def __init__(self, register_file, memory, write_delay=1, fetch=None):
        super().__init__()
        self.register_file = register_file
        self.memory = memory
        self.DELAY = write_delay
        self.current_result = None
        self.current_timer = self.DELAY
        self.future_result = None
        self.future_timer = 0
        self.fetch = fetch

    def feed(self, result):
        """Feed the WriteUnit a Result to write.

        Args:
            result: Result to write.
        """
        assert self.future_result is None, 'WriteUnit fed when full'
        self.future_result = result
        self.future_timer = max(0, self.DELAY - 1)

    def full(self):
        """Return True if the WriteUnit's future state is non-empty."""
        return self.future_result is not None

    def operate(self):
        """Write current Result to the RegisterFile if present and delay done."""
        if self.current_result and self.current_timer == 0:
            typ = self.current_result.typ
            store = self.register_file if typ == Register else self.memory

            store[self.current_result.dest] = self.current_result.value
            if self.future_result is self.current_result:
                self.future_result = None
            if self.fetch is not None:
                self.fetch.pause = False

    def trigger(self):
        """Advance the state of the WriteUnit and init a new future state."""
        # Update current state.
        self.current_result = self.future_result
        self.current_timer = self.future_timer
        # Initialize future state.
        if self.current_result is None:
            self.future_result = None
            self.future_timer = 0
        else:
            self.future_result = self.current_result
            self.future_timer = max(0, self.current_timer - 1)

    def capability(self):
        return Result
