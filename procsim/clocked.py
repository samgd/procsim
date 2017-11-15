import abc

class Clocked(abc.ABC):
    """A Clocked component changes state based on the tick of a Clock.

    Separating the state computation from the state advancement allows a set of
    Clocked instances to interact and compute a new state deterministically
    regardless of the order that the tick method is called on each.
    """

    @abc.abstractmethod
    def operate(self):
        """Compute the future state.

        The Clocked component should compute its own updated future state and
        effect the future state of other components as necessary.
        """
        pass

    @abc.abstractmethod
    def trigger(self):
        """Trigger state change.

        The Clocked component's future state should become its current state
        and a new future state should be initialized.
        """
        pass

    def tick(self):
        """Operate and trigger the clocked component, in that order."""
        self.operate()
        self.trigger()
