import abc

class Tickable(abc.ABC):
    """A Tickle instance changes state based on the tick of a Clock.

    A Tickable should have a current and future state. Other components
    interacting with the Tickable will change the future state only. When tick
    is called, the future state becomes the current state and a new future
    state should be initialized.
    """

    @abc.abstractmethod
    def tick(self):
        pass
