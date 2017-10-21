from procsim.clocked import Clocked

class Fetch(Clocked):
    """Fetch instruction at address in program counter and feed to Decode stage.

    Args:
        register_file: RegisterFile to read program counter value from.
        program_file: File containing assembly program.
        decode: Decode unit to feed Fetched Instruction strings to.
    """

    def __init__(self, register_file, program_file, decode):
        with open(program_file, 'r') as file:
            self.program = file.read().splitlines()
        self.reg_file = register_file
        self.decode = decode

    def operate(self):
        """Fetch next Instruction string, inc pc, and feed Decode if not busy."""
        if not self.decode.busy():
            ins = self.program[self.reg_file['pc']]
            self.decode.feed(ins)
            self.reg_file['pc'] += 1

    def trigger(self):
        pass
