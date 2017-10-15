import abc

class Feedable(abc.ABC):
    """A Feedable instance can be fed."""
    @abc.abstractmethod
    def feed(self):
        pass

    @abc.abstractmethod
    def busy(self):
        pass
