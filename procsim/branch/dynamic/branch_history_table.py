from collections import defaultdict

from procsim.branch.branch_info import BranchInfo
from procsim.branch.predictor import Predictor

class BranchHistoryTable(Predictor):
    """A Branch History Table (BHT) with N prediction bits.

    The saturating counter for each entry is initialized to weakly taken,
    2**(n_prediction_bits - 1).

    Args:
        n_entries: Size of the history table.
        n_prediction_bits: Number of bits to use for the saturating counter.
    """

    def __init__(self, n_entries, n_prediction_bits):
        super().__init__()
        self.n_entries = n_entries
        self.n_prediction_bits = n_prediction_bits
        self.history_table = defaultdict(lambda: 2**(n_prediction_bits - 1))

    def predict(self, program_counter, instruction_str):
        blth = self._parse_conditional(instruction_str)

        counter = self.history_table[program_counter % self.n_entries]
        taken = counter >= 2**(self.n_prediction_bits - 1)

        return BranchInfo(taken, blth.imm, program_counter + 1, program_counter)

    def receive(self, addr, taken):
        idx = addr % self.n_entries
        counter = self.history_table[idx]
        if taken:
            counter += 1
        else:
            counter -= 1
        # Saturating counter.
        counter = max(0, min(2**self.n_prediction_bits - 1, counter))
        self.history_table[idx] = counter
