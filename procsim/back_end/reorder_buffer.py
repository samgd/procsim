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
        # Invariant: head_id's point to first entry in queue. tail_id's point
        # to next free slot in queue.
        self.current_head_id = None
        self.current_tail_id = 0
        self.future_head_id = None
        self.future_tail_id = 0
        self.current_queue = {}
        self.future_queue = {}

        # RAT.
        self.register_alias_table = {}

        # Used during conversion from front_end to back_end instructions.
        self.translate_fn_lookup = {Add:  self._translate_arith_register,
                                    AddI: self._translate_arith_imm,
                                    Sub:  self._translate_arith_register,
                                    SubI: self._translate_arith_imm,
                                    Mul:  self._translate_arith_register,
                                    MulI: self._translate_arith_imm}
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
        start_head_id = self.current_head_id
        while self.current_head_id is not None:
            if self.current_head_id == self.current_tail_id:
                # Tail reached - committed all possible instructions.
                self.current_head_id = None
                break
            if n_commit > 0 and self.current_head_id == start_head_id:
                # Looped back to start - committed all possible instructions.
                self.current_head_id = None
                break
            if n_commit == self.WIDTH:
                # Unable to commit any more this cycle.
                break

            id = self.ID_PREFIX + str(self.current_head_id)
            head = self.current_queue[id]
            if head.value is None:
                # Value still being computed.
                break

            # Write value to RegisterFile and remove from future queue.
            self.register_file[head.dest] = head.value
            del self.future_queue[id]
            # If RAT points to this ROB ID then we can remove the RAT entry as
            # the value is now in the RegisterFile.
            try:
                rat_id = self.register_alias_table[head.dest]
                if rat_id == id:
                    del self.register_alias_table[head.dest]
            except KeyError:
                pass
            # ROB ID now free.
            if self.future_tail_id is None:
                self.future_tail_id = self.current_head_id

            self.current_head_id = (self.current_head_id + 1) % self.CAPACITY
            n_commit += 1

        # Establish invariant.
        if self.current_head_id is not None:
            # future_head_id points to next instruction to commit (when
            # possible).
            self.future_head_id = self.current_head_id
        elif self.future_tail_id == self.current_tail_id:
            # Processed all current instructions and no more have been fed
            # (future_tail_id hasn't moved) so future_head_id had nothing to
            # point to.
            self.future_head_id = None

    def trigger(self):
        """Future queue state becomes the current queue state."""
        self.current_head_id = self.future_head_id
        self.current_tail_id = self.future_tail_id
        self.current_queue = self.future_queue
        self.future_queue = copy(self.current_queue)

    def receive(self, result):
        """Update the value of the QueueEntry ID that matches the result tag."""
        self.future_queue[result.tag].value = result.value

    def _translate_arith_register(self, front_end_ins):
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

    def _translate_arith_imm(self, front_end_ins):
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
        """Allocate and return a ROB ID.

        Returns:
            ROB ID (string).

        Raises:
            AssertionError if no ROB ID available (internal queue is full).
        """
        assert self.future_tail_id is not None,\
            'No free slot in ROB'
        id = self.ID_PREFIX + str(self.future_tail_id)
        # Establish the invariant.
        if self.future_head_id is None:
            self.future_head_id = self.future_tail_id
        self.future_tail_id = (self.future_tail_id + 1) % self.CAPACITY
        if self.future_tail_id == self.future_head_id:
            self.future_tail_id = None
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
