from procsim.clocked import Clocked
from procsim.feedable import Feedable

class WriteUnit(Clocked, Feedable):
    """A WriteUnit writes Results to a RegisterFile after a number of ticks.

    Args:
        register_file: RegisterFile to write results to.
        write_delay: Number of trigger calls to wait before writing a Result to
            the register_file. (default 1)
    """

    def __init__(self, register_file, write_delay=1):
        super().__init__()
        self.register_file = register_file
        self.DELAY = write_delay
        self.current_result = None
        self.current_timer = self.DELAY
        self.future_result = None
        self.future_timer = 0

    def feed(self, result):
        """Feed the WriteUnit a Result to write.

        Args:
            result: Result to write.
        """
        assert self.future_result is None, 'WriteUnit fed when busy'
        self.future_result = result
        self.future_timer = max(0, self.DELAY - 1)

    def busy(self):
        """Return True if the WriteUnit's future state is non-empty."""
        return self.future_result is not None

    def operate(self):
        """Write current Result to the RegisterFile if present and delay done."""
        if self.current_result and self.current_timer == 0:
            self.register_file[self.current_result.dest] = self.current_result.value

    def trigger(self):
        """Advance the state of the WriteUnit and init a new future state."""
        # Update current state.
        self.current_result = self.future_result
        self.current_timer = self.future_timer
        # Initialize future state.
        if self.current_timer == 0:
            self.future_result = None
            self.future_timer = 0
        else:
            self.future_result = self.current_result
            self.future_timer = max(0, self.current_timer - 1)
