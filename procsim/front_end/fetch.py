from procsim.clocked import Clocked
from procsim.branch.branch_info import BranchInfo

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
        branch_predictor: Branch Predictor determines whether to speculative
            take a branch or not.
        width: Maximum number of instructions to fetch and per cycle. Note that
            fewer instructions may be fetched if the Decode unit is full.
            (default 4)
    """

    def __init__(self, register_file, program, decode, branch_predictor, width=4):
        super().__init__()
        self.program = program
        self.reg_file = register_file
        self.decode = decode
        self.branch_predictor = branch_predictor
        self.width = width

    def _fetch_next(self):
        """Return next Instruction string and increment pc if possible.

        Returns: Dictionary containing an instruction_str key or None if no
            instruction can be fetched.
        """
        program_counter = self.reg_file['pc']
        if not self.decode.full() and program_counter < len(self.program):
            ins = self.program[program_counter]
            food = {'instruction_str': ins}
            # Branch detection and handling.
            if ins[0] == 'j':
                self.reg_file['pc'] = self._parse_unconditional_address(ins)
                return None
            elif ins[:4] == 'blth':
                branch_info = self.branch_predictor.predict(program_counter, ins)
                if branch_info.taken:
                    self.reg_file['pc'] = branch_info.taken_addr
                else:
                    self.reg_file['pc'] = branch_info.not_taken_addr
                food['branch_info'] = branch_info
            else:
                self.reg_file['pc'] += 1
            return food

    def operate(self):
        """Feed Decode unit with up to width instructions."""
        for _ in range(self.width):
            food = self._fetch_next()
            if food is None:
                return
            self.decode.feed(food)

    def _parse_unconditional_address(self, uncond_branch):
        """Return target address of unconditional branch."""
        fields = uncond_branch.split(' ')
        return int(fields[1])

    def trigger(self):
        pass

    def flush(self):
        self.decode.flush()
