from procsim.branch.branch_info import BranchInfo
from procsim.branch.predictor import Predictor

class BackTakenForwardNot(Predictor):
    """A Predictor that only predicts taken if branch points backwards."""

    def __init__(self):
        super().__init__()

    def predict(self, program_counter, instruction_str):
        blth = self._parse_conditional(instruction_str)
        take = blth.imm < program_counter
        return BranchInfo(take, blth.imm, program_counter + 1)
