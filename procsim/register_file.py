from procsim.register import Register

class RegisterFile:
    """A RegisterFile containing general purpose Registers and a program counter.

    The program counter is indexed using 'pc'.

    Args:
        n_gpr_registers: Number of general purpose Registers in the
            RegisterFile.
        gpr_prefix: Prefix added to each general purpose Register index to form
            the Register name. General purpose Register indicies start from 0.
            (default 'r')
        init_values: {register_name: value} dict to initialize the Register
            values from.
    """
    def __init__(self, n_gpr_registers, gpr_prefix='r', init_values=None):
        self.prefix = gpr_prefix
        self.registers = {gpr_prefix + str(i): Register()
                          for i in range(n_gpr_registers)}
        self.registers['pc'] = Register()
        if init_values is not None:
            for name, value in init_values.items():
                self[name] = value

    def __eq__(self, other):
        """Return True if all Register values are equal."""
        return self.registers == other.registers

    def __getitem__(self, name):
        """Get a Register's value."""
        return self.registers[name].read()

    def __setitem__(self, name, value):
        """Set a Register's value."""
        self.registers[name].write(value)

    def __len__(self):
        """Return the number of Registers in the RegisterFile."""
        return len(self.registers)

    def __repr__(self):
        return 'RegisterFile(%d, gpr_prefix=%r, init_values=%r)' % (len(self.registers) - 1,
                                                                    self.prefix,
                                                                    self.registers)
