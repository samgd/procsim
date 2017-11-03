from procsim.clocked import Clocked

class Clock:
    """Simple processor clock to coordinate Clocked component execution.

    Attributes:
        n_ticks: Total number of tick calls.
    """

    def __init__(self):
        self.components = []
        self.n_ticks = 0

    def register(self, component):
        """Register a Clocked component with the Clock."""
        self.components.append(component)

    def operate(self):
        """Call operate on every registered component."""
        for comp in self.components:
            comp.operate()

    def trigger(self):
        """Call trigger on every registered component."""
        for comp in self.components:
            comp.trigger()

    def tick(self):
        """Call operate and trigger on every registered component.

        Operate is called on every registered component first and then trigger
        is called.
        """
        self.operate()
        self.trigger()
        self.n_ticks += 1
