from procsim.branch.predictor import Predictor

class NeverTaken(Predictor):
    """A Predictor that always predicts never taken."""

    def __init__(self):
        super().__init__()

    def predict(self, program_counter):
        return program_counter + 1
