import abc

from procsim.front_end.instructions.blth import Blth

class Predictor(abc.ABC):
    """A Predictor predicts the result of a conditional branch instruction."""

    @abc.abstractmethod
    def predict(self, program_counter, instruction_str):
        """Return BranchInfo about the branch."""
        pass

    @abc.abstractmethod
    def receive(self, addr, taken):
        """Receive information whether the branch at addr was taken or not."""
        pass

    def _parse_conditional(self, instruction_str):
        """Return a Blth instruction."""
        fields = instruction_str.split(' ')
        if fields[0] != 'blth':
            raise ValueError('unable to parse %r' % instruction_str)
        return Blth(fields[1], fields[2], int(fields[3]))
