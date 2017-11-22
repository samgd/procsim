from procsim.flushable import Flushable

class FlushableLog(Flushable):
    """Flushable logs the number of times flush is called.

    Attributes:
        n_flush: Number of times flush has been called.
    """
    def __init__(self):
        self.n_flush = 0

    def flush(self):
        self.n_flush += 1

    def reset(self):
        self.n_flush = 0
