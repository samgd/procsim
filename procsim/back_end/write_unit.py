from procsim.tickable import Tickable
from procsim.feedable import Feedable

class WriteUnit(Tickable, Feedable):
    """A WriteUnit writes Results to a RegisterFile after a number of ticks.

    Args:
        register_file: RegisterFile to write results to.
        write_delay: Number of tick calls to wait before writing a Result to
            the register_file. (default 1)
    """

    def __init__(self, register_file, write_delay=1):
        self.register_file = register_file
        self.result = None
        self.DELAY = write_delay
        self.write_timer = self.DELAY

    def feed(self, result):
        """Feed the WriteUnit a Result to write.

        Args:
            result: Result to write.
        """
        assert self.result is None, 'WriteUnit fed when busy'
        self.result = result
        self.write_timer = self.DELAY

    def busy(self):
        """Return True if the WriteUnit is already waiting to write a Result."""
        return self.result is not None

    def tick(self):
        """Write the Result to the RegisterFile if write_delay reaches 0."""
        self.write_timer = max(0, self.write_timer - 1)
        if self.result and self.write_timer == 0:
            self.register_file[self.result.dest] = self.result.value
            self.result = None
