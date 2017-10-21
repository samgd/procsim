from collections import defaultdict
from copy import copy
from itertools import filterfalse
import inspect

from procsim.pipeline_stage import PipelineStage

class ReservationStation(PipelineStage):
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
        """Issue fed Instructions to capable and non-busy ExecutionUnits.

        Raises:
            AssertionError if no ExecutionUnits exist that are capable of
            executing the Instruction.
        """
        for instruction in self.current_buffer:
            units_exist = False   # If no units exist for instruction, error.
            # Iterate from most to least specific capability.
            for capability in inspect.getmro(type(instruction)):
                units = self.execution_units[capability]
                units_exist |= len(units) > 0
                free_units = {unit for unit in units if not unit.busy()}
                if len(free_units) < 1:
                    continue
                unit = next(iter(free_units))
                unit.feed(instruction)
                self.future_buffer.remove(instruction)
                break
            assert units_exist, 'Instruction %r has no ExecutionUnit' % instruction

    def trigger(self):
        """Free up buffer space by removing the issued Instructions."""
        self.current_buffer = self.future_buffer
        self.future_buffer = copy(self.current_buffer)

    def register(self, execution_unit):
        """Enable the ReservationStation to issue Instructions to the unit.

        Args:
            exectuion_unit: ExecutionUnit to register with the
                ReservationStation.
        """
        self.execution_units[execution_unit.capability()].add(execution_unit)
