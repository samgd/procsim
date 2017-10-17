class Memory:
    """Simple random-access memory model.

    Memory values are initialized to None.

    Args:
        size: Number of addressable locations.
    """

    def __init__(self, size):
        if size <= 0:
            raise ValueError('memory size must be > 0')
        self.memory = [None] * size

    def __len__(self):
        """Return the number of addressable locations."""
        return len(self.memory)

    def __getitem__(self, address):
        """Get the value at the given Memory address."""
        self._validate_address(address)
        return self.memory[address]

    def __setitem__(self, address, value):
        """Set the value at the given Memory address."""
        self._validate_address(address)
        self.memory[address] = value

    def _validate_address(self, address):
        if not isinstance(address, int):
            raise TypeError('memory address must be an integer, not %s', type(address))
        if not 0 <= address < len(self.memory):
            raise IndexError('memory address out of range')
