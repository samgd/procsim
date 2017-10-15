from copy import deepcopy

from procsim.register import Register
from procsim.tickable import Tickable

class RegisterFile(Tickable):
    """A RegisterFile is a set of Registers.

    Note: Register writes only commit after a tick.

    Args:
        n_registers: Number of registers in the RegisterFile.
        prefix: Prefix added to each Register index to form the Register
            name. Register indicies start from 0. (default 'r')
        init_values: {register_name: value} dict to initialize the Register
            values from.
    """
    def __init__(self, n_registers, prefix='r', init_values=None):
        self.prefix = prefix
        self.current = {prefix + str(i): Register() for i in range(n_registers)}
        if init_values is not None:
            for name, value in init_values.items():
                self.current[name].write(value)
        self.future = self._initialize_future()

    def __eq__(self, other):
        """Return True if all current Register values are equal."""
        return self.current == other.current

    def __getitem__(self, name):
        """Get a Register."""
        # Defensive copy to prevent modification avoiding tickable.
        return deepcopy(self.current[name])

    def __setitem__(self, name, value):
        """Set a Register's value on next tick."""
        self.future[name].write(value)

    def __len__(self):
        """Return the number of Registers in the RegisterFile."""
        return len(self.current)

    def __repr__(self):
        return 'RegisterFile(%d, prefix=%r, init_values=%r)' % (len(self.current),
                                                                self.prefix,
                                                                self.current)
    def tick(self):
        self.current = self.future
        self.future = self._initialize_future

    def _initialize_future(self):
        """Return a deepcopy of the current state."""
        return deepcopy(self.current)
