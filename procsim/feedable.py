import abc

class Feedable(abc.ABC):
    """A Feedable instance can be fed."""
    @abc.abstractmethod
    def feed(self, food):
        """Feed food to the Feedable.

        Args:
            food: Food to be fed.
        """
        pass

    @abc.abstractmethod
    def full(self):
        """Return True if the Feedable can be fed no more food.

        Returns:
            Boolean that is True if no more food should be fed.
        """
        pass
