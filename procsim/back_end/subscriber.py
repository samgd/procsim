import abc

class Subscriber(abc.ABC):
    """A Subscriber to a BroadcastBus."""

    @abc.abstractmethod
    def receive(self, message):
        """Receive a message from a BroadcastBus

        Args:
            message: Published message to receive.
        """
        pass
