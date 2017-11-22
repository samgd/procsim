from procsim.clocked import Clocked
from procsim.front_end.branch_info import BranchInfo

class Fetch(Clocked):
    """Fetch instruction at address in program counter and feed to Decode stage.

    The Fetch unit has logic to detect conditional branch instructions. It will
    tag each with a branch_info attribute that has a BranchInfo object as value.

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
        """Fetch next Instruction string, inc pc, and feed Decode if not full."""
        program_counter = self.reg_file['pc']
        if not self.pause and not self.decode.full() and program_counter < len(self.program):
            ins = self.program[program_counter]
            food = {'instruction_str': ins}
            try:
                branch_info = self._parse_branch_info(ins, program_counter + 1)
                food['branch_info'] = branch_info
            except:
                pass
            self.decode.feed(food)
            self.reg_file['pc'] += 1
            if self.sequential:
                self.pause = True

    def _parse_branch_info(self, cond_branch, next_pc):
        """Return BranchInfo for a conditional branch instruction."""
        fields = cond_branch.split(' ')
        if fields[0] != 'blth':
            raise ValueError('instruction is not a conditional branch')
        return BranchInfo(False, int(fields[3]), next_pc)

    def trigger(self):
        pass
