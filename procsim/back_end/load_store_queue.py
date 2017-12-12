from copy import copy

from procsim.back_end.instructions.load import Load
from procsim.back_end.instructions.memory_access import MemoryAccess
from procsim.back_end.instructions.store import Store
from procsim.back_end.result import Result
from procsim.back_end.subscriber import Subscriber
from procsim.pipeline_stage import PipelineStage

class LoadStoreQueue(PipelineStage, Subscriber):
    """In-order LoadStoreQueue.

    Args:
        memory: Memory instructions should execute on.
        broadcast_bus: BroadcastBus to publish Results to.
        capacity: Size of the queue. (Max MemoryAccess Instructions that can be
            contained within the LoadStoreQueue at any one time.)
        data_forwarding: If True, Stores forward results to later Loads.
    """

    def __init__(self, memory, broadcast_bus, capacity=32, width=4, data_forwarding=True):
        super().__init__()
        if capacity < 1:
            raise ValueError('capacity must be >= 1')
        self.CAPACITY = capacity
        self.width = width
        self.memory = memory
        self.broadcast_bus = broadcast_bus
        self.spec_exec = {}
        self.current_queue = []
        self.future_queue = []
        self.data_forwarding = data_forwarding

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
        self.spec_exec[instruction.uid] = instruction.spec_exec

    def speculative_execution_off(self, uid):
        """Turn off the speculative execution status of an Instruction.

        Args:
            uid: UID of Instruction whose status to change to not speculative.
        """
        self.spec_exec[uid] = False

    def full(self):
        """Return True if the LoadStoreQueue is full.

        Returns:
            True if the LoadStoreQueue is unable to be fed more Instructions.
        """
        return len(self.future_queue) == self.CAPACITY

    def operate(self):
        n_op = 0
        next_idx = 0
        unk_addr = set()

        while len(self.current_queue) > next_idx and n_op < self.width:
            n_op += 1

            entry = self.current_queue[next_idx]
            if self.spec_exec[entry.uid] or not entry.can_dispatch():
                if isinstance(entry, Store):
                    # Store with unknown address blocks rest.
                    if entry.address is None:
                        return
                    # Store with known address but not value permits later
                    # loads and stores to operate provided they have different
                    # addresses.
                    unk_addr.add(entry.address)
                next_idx += 1
                continue

            if entry.address in unk_addr:
                next_idx += 1
                continue

            entry.DELAY = max(0, entry.DELAY - 1)
            if entry.DELAY > 0 and not hasattr(entry, 'forwarded'):
                next_idx += 1
                continue

            result = entry.execute(self.memory)
            if result:
                self.broadcast_bus.publish(result)
            del self.spec_exec[entry.uid]
            del self.current_queue[next_idx]
            del self.future_queue[next_idx]
            if self.data_forwarding:
                self._data_forward(entry)

    def _data_forward(self, ins):
        """Forward Store value to Load instructions."""
        if not isinstance(ins, Store):
            return
        for queue_ins in self.current_queue:
            if queue_ins.address == ins.address:
                if isinstance(queue_ins, Store):
                    break
                queue_ins.forwarded = True

    def trigger(self):
        """Free up queue space by removing the executed Instructions."""
        self.current_queue = self.future_queue
        self.future_queue = copy(self.current_queue)

    def receive(self, result):
        for instruction in self.current_queue:
            instruction.receive(result)

    def flush(self):
        self.current_queue = [ins for ins in self.current_queue if not self.spec_exec[ins.uid]]
        self.future_queue = [ins for ins in self.future_queue if not self.spec_exec[ins.uid]]
        self.spec_exec = {ins.uid: False for ins in self.future_queue}
