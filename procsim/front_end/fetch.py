from procsim.clocked import Clocked
from procsim.front_end.branch_info import BranchInfo

class Fetch(Clocked):
    """Fetch instruction at address in program counter and feed to Decode stage.

    The Fetch unit has logic to detect branch instructions. It will tag each
    conditional branch instruction with a branch_info attribute that has a
    BranchInfo object as value. It will set the pc to the given value for an
    unconditional branch.

    Args:
        register_file: RegisterFile to read program counter value from.
        program: List of string Instructions.
        decode: Decode unit to feed Fetched Instruction strings to.
    """

    def __init__(self, register_file, program, decode):
        super().__init__()
        self.program = program
        self.reg_file = register_file
        self.decode = decode

    def operate(self):
        """Fetch next Instruction string, inc pc, and feed Decode if not full."""
        program_counter = self.reg_file['pc']
        if not self.decode.full() and program_counter < len(self.program):
            ins = self.program[program_counter]
            food = {'instruction_str': ins}
            # Branch detection and handling.
            if ins[0] == 'j':
                self.reg_file['pc'] = self._parse_unconditional_address(ins)
                return
            elif ins[:4] == 'blth':
                branch_info = self._parse_conditional_branch_info(ins, program_counter + 1)
                food['branch_info'] = branch_info
            self.decode.feed(food)
            self.reg_file['pc'] += 1

    def _parse_unconditional_address(self, uncond_branch):
        """Return target address of unconditional branch."""
        fields = uncond_branch.split(' ')
        return int(fields[1])

    def _parse_conditional_branch_info(self, cond_branch, next_pc):
        """Return BranchInfo for a conditional branch instruction."""
        fields = cond_branch.split(' ')
        if fields[0] != 'blth':
            raise ValueError('instruction is not a conditional branch')
        return BranchInfo(False, int(fields[3]), next_pc)

    def trigger(self):
        pass

    def flush(self):
        self.decode.flush()
