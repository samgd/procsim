import abc

class Predictor(abc.ABC):
    """A Predictor predicts the result of a conditional branch instruction."""

    @abc.abstractmethod
    def predict(self, program_counter):
        """Return the address of the predicted outcome of the branch."""
        pass
