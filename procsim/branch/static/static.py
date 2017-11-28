from procsim.branch.predictor import Predictor

class Static(Predictor):
    """A Static Predictor ignores all received information."""

    def __init__(self):
        super().__init__()

    def receive(self, addr, taken):
        pass
