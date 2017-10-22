from procsim.clocked import Clocked

class Fetch(Clocked):
    """Fetch instruction at address in program counter and feed to Decode stage.

    Args:
        register_file: RegisterFile to read program counter value from.
        program_file: File containing assembly program.
        decode: Decode unit to feed Fetched Instruction strings to.
    """

    def __init__(self, register_file, program_file, decode):
        super().__init__()
        with open(program_file, 'r') as prog:
            self.program = prog.read().splitlines()
        self.reg_file = register_file
        self.decode = decode

    def operate(self):
        """Fetch next Instruction string, inc pc, and feed Decode if not busy."""
        program_counter = self.reg_file['pc']
        if not self.decode.busy() and program_counter < len(self.program):
            ins = self.program[program_counter]
            self.decode.feed(ins)
            self.reg_file['pc'] += 1

    def trigger(self):
        pass
