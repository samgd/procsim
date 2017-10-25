from procsim.clocked import Clocked

class Fetch(Clocked):
    """Fetch instruction at address in program counter and feed to Decode stage.

    Args:
        register_file: RegisterFile to read program counter value from.
        program: List of string Instructions.
        decode: Decode unit to feed Fetched Instruction strings to.
        sequential: If True operate sets pause to True after every call. This
            WILL BE DEPRECIATED once pipelining has been implemented.

    Attributes:
        pause: Bool that pauses the Fetch unit's operation. This WILL BE
            DEPRECIATED once pipelining has been implemented.
    """

    def __init__(self, register_file, program, decode, sequential=False):
        super().__init__()
        self.program = program
        self.reg_file = register_file
        self.decode = decode
        self.pause = False
        self.sequential = sequential

    def operate(self):
        """Fetch next Instruction string, inc pc, and feed Decode if not busy."""
        program_counter = self.reg_file['pc']
        if not self.pause and not self.decode.busy() and program_counter < len(self.program):
            ins = self.program[program_counter]
            self.decode.feed(ins)
            self.reg_file['pc'] += 1
            if self.sequential:
                self.pause = True

    def trigger(self):
        pass
