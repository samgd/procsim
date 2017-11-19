from copy import copy

from procsim.back_end.instructions.load import Load
from procsim.back_end.instructions.memory_access import MemoryAccess
from procsim.back_end.instructions.store import Store
from procsim.back_end.subscriber import Subscriber
from procsim.pipeline_stage import PipelineStage

class LoadStoreQueue(PipelineStage, Subscriber):
    """In-order LoadStoreQueue.

    Args:
        broadcast_bus: BroadcastBus to publish Results to.
        capacity: Size of the queue. (Max MemoryAccess Instructions that can be
            contained within the LoadStoreQueue at any one time.)
    """

    def __init__(self, memory, broadcast_bus, capacity=32):
        super().__init__()
        if capacity < 1:
            raise ValueError('capacity must be >= 1')
        self.CAPACITY = capacity
        self.memory = memory
        self.broadcast_bus = broadcast_bus
        self.current_queue = []
        self.future_queue = []

    def feed(self, instruction):
        """Insert a MemoryAccess Instruction into the LoadStoreQueue.

        Args:
            instruction: MemoryAccess Instruction to insert.
        """
        assert len(self.future_queue) < self.CAPACITY,\
            'LoadStoreQueue fed when full'
        assert isinstance(instruction, MemoryAccess),\
            'LoadStoreQueue fed non-MemoryAccess Instruction'
        self.future_queue.append(instruction)

    def full(self):
        """Return True if the LoadStoreQueue is full.

        Returns:
            True if the LoadStoreQueue is unable to be fed more Instructions.
        """
        return len(self.future_queue) == self.CAPACITY

    def operate(self):
        if len(self.current_queue) == 0:
            return
        head = self.current_queue[0]
        if not head.can_execute():
            return
        head.DELAY = max(0, head.DELAY - 1)
        if head.DELAY > 0 and isinstance(head, Load):
            return
        args = (self.memory,) if isinstance(head, Load) else ()
        result = head.execute(*args)
        self.broadcast_bus.publish(result)
        del self.current_queue[0]
        del self.future_queue[0]

    def trigger(self):
        """Free up queue space by removing the executed Instructions."""
        self.current_queue = self.future_queue
        self.future_queue = copy(self.current_queue)

    def receive(self, result):
        for instruction in self.current_queue:
            instruction.receive(result)
