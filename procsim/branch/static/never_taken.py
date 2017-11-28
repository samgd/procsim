from procsim.branch.branch_info import BranchInfo
from procsim.branch.static.static import Static

class NeverTaken(Static):
    """A Static Predictor that always predicts never taken."""

    def __init__(self):
        super().__init__()

    def predict(self, program_counter, instruction_str):
        blth = self._parse_conditional(instruction_str)
        return BranchInfo(False, blth.imm, program_counter + 1, program_counter)
