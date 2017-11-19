from collections import defaultdict
from copy import copy
from itertools import filterfalse
import inspect

from procsim.back_end.subscriber import Subscriber
from procsim.pipeline_stage import PipelineStage

class ReservationStation(PipelineStage, Subscriber):
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
        """Insert an Instruction into the ReservationStation.

        Args:
            instruction: Instruction to insert.
        """
        assert len(self.future_buffer) < self.CAPACITY,\
            'ReservationStation fed when full'
        self.future_buffer.add(instruction)

    def full(self):
        """Return True if the ReservationStation is full.

        Returns:
            True if the ReservationStation is unable to be fed more
            Instructions.
        """
        return len(self.future_buffer) == self.CAPACITY

    def operate(self):
        """Issue fed Instructions to capable and non-full ExecutionUnits.

        Raises:
            AssertionError if no ExecutionUnits exist that are capable of
            executing the Instruction.
        """
        for instruction in self.current_buffer:
            if not instruction.can_dispatch():
                continue
            exist = False
            for cap in inspect.getmro(type(instruction)):
                units = self.execution_units[cap]
                exist = exist or units

                idle = {u for u in units if not u.full()}
                if idle:
                    unit = next(iter(idle))
                    unit.feed(instruction)
                    self.future_buffer.remove(instruction)
                    break
            assert exist, 'Instruction %r has no ExecutionUnit' % instruction

    def trigger(self):
        """Free up buffer space by removing the issued Instructions."""
        self.current_buffer = self.future_buffer
        self.future_buffer = copy(self.current_buffer)

    def register(self, execution_unit):
        """Enable the ReservationStation to issue Instructions to the unit.

        Args:
            execution_unit: ExecutionUnit to register with the
                ReservationStation.
        """
        self.execution_units[execution_unit.capability()].add(execution_unit)

    def receive(self, result):
        for instruction in self.current_buffer:
            instruction.receive(result)
