import abc

class Flushable(abc.ABC):
    """A Flushable can be flushed.

    Each Flushable is a node in a Flushable tree and must ensure to propagate
    the flush to all Flushable nodes below it.
    """

    @abc.abstractmethod
    def flush(self):
        """Flush the Flushable and propagate the flush down the Flushable tree."""
        pass
