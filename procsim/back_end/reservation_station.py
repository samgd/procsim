from collections import defaultdict

from procsim.back_end.execution_unit import ExecutionUnit
from procsim.clocked import Clocked
from procsim.feedable import Feedable

class ReservationStation(Clocked, Feedable):
    """A ReservationStation that buffers Instructions until all of their
    execution requirements are met.

    Args:
        capacity: Size of the buffer.  (Max Instructions that can be contained
            within the ReservationStation at any one time.)
    """

    def __init__(self, capacity=32):
        super().__init__()
        self.execution_units = defaultdict(set)
        if capacity < 1:
            raise ValueError('capacity must be >= 1')
        self.CAPACITY = capacity
        self.current_buffer = set()
        self.future_buffer = set()

    def feed(self, instruction):
        """Insert an Instruction to the ReservationStation.

        Args:
            instruction: Instruction to insert.
        """
        assert len(self.future_buffer) < self.CAPACITY, 'ReservationStation fed when busy'
        self.future_buffer.add(instruction)

    def busy(self):
        """Return True if the ReservationStation is full (Instructions)."""
        return len(self.future_buffer) == self.CAPACITY

    def operate(self):
        """Issue fed Instructions to capable and non-busy ExecutionUnits."""
        pass

    def trigger(self):
        """Free up buffer space by removing the issued Instructions."""
        pass

    def register(self, execution_unit):
        """Enable the ReservationStation to issue Instructions to the unit.

        Args:
            exectuion_unit: ExecutionUnit to register with the
                ReservationStation.
        """
        self.execution_units[execution_unit.capability()].add(execution_unit)
