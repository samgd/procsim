from procsim.register import Register

class RegisterFile:
    """A RegisterFile is a set of Registers.

    Args:
        n_registers: Number of registers in the RegisterFile.
        prefix: Prefix added to each Register index to form the Register
            name. Register indicies start from 0. (default 'r')
        init_values: {register_name: value} dict to initialize the Register
            values from.
    """
    def __init__(self, n_registers, prefix='r', init_values=None):
        self.prefix = prefix
        self.registers = {prefix + str(i): Register() for i in range(n_registers)}
        if init_values is not None:
            for name, value in init_values.items():
                self[name] = value

    def __eq__(self, other):
        """Return True if all Register values are equal."""
        return self.registers == other.registers

    def __getitem__(self, name):
        """Get a Register."""
        return self.registers[name]

    def __setitem__(self, name, value):
        """Set a Register's value."""
        self.registers[name].write(value)

    def __len__(self):
        """Return the number of Registers in the RegisterFile."""
        return len(self.registers)

    def __repr__(self):
        return 'RegisterFile(%d, prefix=%r, init_values=%r)' % (len(self.registers),
                                                                self.prefix,
                                                                self.registers)
