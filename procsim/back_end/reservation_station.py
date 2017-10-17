from collections import defaultdict

from procsim.back_end.execution_unit import ExecutionUnit
from procsim.clocked import Clocked
from procsim.feedable import Feedable

class ReservationStation(Clocked, Feedable):

    def __init__(self):
        super().__init__()
        self.execution_units = defaultdict(set)

    def feed(self, instruction):
        """Insert an Instruction to the ReservationStation.

        Args:
            instruction: Instruction to insert.
        """
        pass

    def busy(self):
        """Return True if the ReservationStation is full."""
        pass

    def operate(self):
        pass

    def trigger(self):
        pass

    def register(self, execution_unit):
        """Enable the ReservationStation to issue Instructions to the unit.

        Args:
            exectuion_unit: ExecutionUnit to register with the
                ReservationStation.
        """
        self.execution_units[execution_unit.capability()].add(execution_unit)
