from copy import copy

from procsim.back_end.instructions.integer_logical import IntegerLogical
from procsim.back_end.subscriber import Subscriber
from procsim.front_end.instructions import *
from procsim.pipeline_stage import PipelineStage

class ReorderBuffer(PipelineStage, Subscriber):
    """A ReorderBuffer that facilitates out-of-order instruction execution.

    Args:
        register_file: RegisterFile to read values from.
        reservation_station: ReservationStation to feed backend Instructions to.
        capacity: Size of the buffer.  (Max Instructions that can be contained
            within the ReorderBuffer at any one time.)
    """

    def __init__(self, register_file, reservation_station, capacity=32):
        super().__init__()
        self.register_file = register_file
        self.reservation_station = reservation_station
        # Superscalar width.
        self.WIDTH = 4

        # Circular queue setup.
        if capacity < 1:
            raise ValueError('capacity must be >= 1')
        self.CAPACITY = capacity
        self.ID_PREFIX = 'ROB'
        self.current_head_id = 0
        self.current_tail_id = 0
        self.future_head_id = 0
        self.future_tail_id = 0
        self.current_queue = {}
        self.future_queue = {}

        # RAT.
        self.register_alias_table = {}

        # Used during conversion from front_end to back_end instructions.
        self.translate_fn_lookup = {Add:  self.translate_arith_register,
                                    AddI: self.translate_arith_imm,
                                    Sub:  self.translate_arith_register,
                                    SubI: self.translate_arith_imm,
                                    Mul:  self.translate_arith_register,
                                    MulI: self.translate_arith_imm}
        self.operation_lookup = {Add:  lambda o1, o2: o1 + o2,
                                 AddI: lambda o1, o2: o1 + o2,
                                 Sub:  lambda o1, o2: o1 - o2,
                                 SubI: lambda o1, o2: o1 - o2,
                                 Mul:  lambda o1, o2: o1 * o2,
                                 MulI: lambda o1, o2: o1 * o2}

    def feed(self, front_end_ins):
        """Insert an Instruction into the ReorderBuffer.

        Args:
            front_end_ins: Frontend instruction to insert.
        """
        assert (len(self.future_queue) < self.CAPACITY
                and not self.reservation_station.full()), \
                'ReorderBuffer fed when full'

        translate = self.translate_fn_lookup[type(front_end_ins)]
        back_end_ins = translate(front_end_ins)
        self.reservation_station.feed(back_end_ins)
        self.future_queue[back_end_ins.tag] = QueueEntry(front_end_ins.rd, None)

    def full(self):
        """Return True if the ReorderBuffer is full.

        Returns:
            True if the ReorderBuffer is unable to be fed more instructions.
        """
        return (len(self.future_queue) == self.CAPACITY
                or self.reservation_station.full())

    def operate(self):
        """Commit, in-order, completed instructions."""
        n_commit = 0
        while n_commit < self.WIDTH and self.future_head_id != self.current_tail_id:
            # Head QueueEntry.
            id = self.ID_PREFIX + str(self.future_head_id)
            head = self.current_queue[id]
            # Value still being computed.
            if head.value is None:
                return
            # Write value to RegisterFile and remove from future queue.
            self.register_file[head.dest] = head.value
            del self.future_queue[id]
            # If RAT points to this ROB id then we can remove the RAT entry as
            # the value is now in the RegisterFile.
            try:
                rat_id = self.register_alias_table[head.dest]
                if rat_id == id:
                    del self.register_alias_table[head.dest]
            except KeyError:
                pass
            self.future_head_id = (self.future_head_id + 1) % self.CAPACITY
            n_commit += 1

    def trigger(self):
        """Future queue state becomes the current queue state."""
        self.current_head_id = self.future_head_id
        self.current_tail_id = self.future_tail_id
        self.current_queue = self.future_queue
        self.future_queue = copy(self.current_queue)

    def receive(self, result):
        """Update the value of the QueueEntry ID that matches the result tag."""
        self.future_queue[result.tag].value = result.value

    def translate_arith_register(self, front_end_ins):
        """Return a backend Instruction formed from a frontend instruction.

        This function will increment the ReorderBuffer's future queue tail
        pointer.

        Args:
            front_end_ins: Register-form arithmetic frontend instruction.

        Returns:
            IntegerLogical instruction.
        """
        queue_id = self._get_queue_id()

        operand_1 = self._translate_operand(front_end_ins.r1)
        operand_2 = self._translate_operand(front_end_ins.r2)

        self.register_alias_table[front_end_ins.rd] = queue_id

        return IntegerLogical(queue_id,
                              self.operation_lookup[type(front_end_ins)],
                              operand_1,
                              operand_2)

    def translate_arith_imm(self, front_end_ins):
        """Return a backend Instruction formed from a frontend instruction.

        This function will increment the ReorderBuffer's future queue tail
        pointer.

        Args:
            front_end_ins: Immediate-form arithmetic frontend instruction.

        Returns:
            IntegerLogical instruction.
        """
        queue_id = self._get_queue_id()

        operand_1 = self._translate_operand(front_end_ins.r1)
        operand_2 = front_end_ins.imm

        self.register_alias_table[front_end_ins.rd] = queue_id

        return IntegerLogical(queue_id,
                              self.operation_lookup[type(front_end_ins)],
                              operand_1,
                              operand_2)

    def _get_queue_id(self):
        """Allocate and return a ROB queue ID."""
        id = self.ID_PREFIX + str(self.future_tail_id)
        self.future_tail_id = (self.future_tail_id + 1) % self.CAPACITY
        return id

    def _translate_operand(self, register_name):
        """Convert the register name to an operand (value or ROB ID).

        Returns:
            Value stored in register_name or the ID of a QueueEntry in the ROB
            that will yield the value.
        """
        if register_name in self.register_alias_table:
            return self.register_alias_table[register_name]
        return self.register_file[register_name]

class QueueEntry:
    """An entry in a ReorderBuffer's circular queue.

    Attributes:
        dest: Target to store value in.
        value: Value to save to dest. None indicates that it is still to be
            computed by the processor. (default None)
    """

    def __init__(self, dest, value=None):
        self.dest = dest
        self.value = value

    def __repr__(self):
        return 'QueueEntry(%r, %r)' % (self.dest, self.value)
