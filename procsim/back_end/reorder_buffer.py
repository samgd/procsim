from copy import copy

from procsim.back_end.instructions.integer_logical import IntegerLogical
from procsim.back_end.subscriber import Subscriber
from procsim.front_end.instructions import *
from procsim.pipeline_stage import PipelineStage

class ReorderBuffer(PipelineStage, Subscriber):

    def __init__(self, register_file, reservation_station, capacity=32):
        super().__init__()
        self.register_file = register_file
        self.reservation_station = reservation_station

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

        self.register_alias_table = {}

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
        assert (len(self.future_queue) < self.CAPACITY
                and not self.reservation_station.full()), \
                'ReorderBuffer fed when full'

        translate = self.translate_fn_lookup[type(front_end_ins)]
        back_end_ins = translate(front_end_ins)
        # Insert into RS
        self.reservation_station.feed(back_end_ins)
        # Insert into future ROB queue.
        self.future_queue[back_end_ins.tag] = QueueEntry(front_end_ins.rd, None)

    def translate_arith_register(self, front_end_ins):
        """front_end.instruction -> back_end.instruction"""
        # Get ROB_id
        queue_id = self._get_queue_id()

        # Convert operands using RAT if registers.
        if front_end_ins.r1 in self.register_alias_table:
            operand_1 = self.register_alias_table[front_end_ins.r1]
        else:
            operand_1 = self.register_file[front_end_ins.r1]

        if front_end_ins.r2 in self.register_alias_table:
            operand_2 = self.register_alias_table[front_end_ins.r2]
        else:
            operand_2 = self.register_file[front_end_ins.r2]

        # Update RAT entry.
        self.register_alias_table[front_end_ins.rd] = queue_id

        # Create back_end instruction.
        return IntegerLogical(queue_id,
                              self.operation_lookup[type(front_end_ins)],
                              operand_1,
                              operand_2)

    def translate_arith_imm(self, front_end_ins):
        """front_end.instruction -> back_end.instruction"""
        # Get ROB_id
        queue_id = self._get_queue_id()

        # Convert operands using RAT if registers.
        if front_end_ins.r1 in self.register_alias_table:
            operand_1 = self.register_alias_table[front_end_ins.r1]
        else:
            operand_1 = self.register_file[front_end_ins.r1]

        operand_2 = front_end_ins.imm

        # Update RAT entry.
        self.register_alias_table[front_end_ins.rd] = queue_id

        # Create back_end instruction.
        return IntegerLogical(queue_id,
                              self.operation_lookup[type(front_end_ins)],
                              operand_1,
                              operand_2)

    def full(self):
        return (len(self.future_queue) == self.CAPACITY
                or self.reservation_station.full())

    def operate(self):
        while self.future_head_id != self.current_tail_id:
            # Get head QueueEntry.
            id = self.ID_PREFIX + str(self.future_head_id)
            head = self.current_queue[id]
            # Return if value still being computed.
            if head.value is None:
                return
            # Write value to RegisterFile.
            self.register_file[head.dest] = head.value
            # Remove from future queue now value is written.
            del self.future_queue[id]
            # If RAT points to this ROB id then we can remove the RAT entry as
            # the value is now in the RegisterFile anyway!
            try:
                rat_id = self.register_alias_table[head.dest]
                if rat_id == id:
                    del self.register_alias_table[head.dest]
            except KeyError:
                pass
            self.future_head_id = (self.future_head_id + 1) % self.CAPACITY

    def trigger(self):
        self.current_head_id = self.future_head_id
        self.current_tail_id = self.future_tail_id
        self.current_queue = self.future_queue
        self.future_queue = copy(self.current_queue)

    def receive(self, result):
        self.future_queue[result.tag].value = result.value

    def _get_queue_id(self):
        id = self.ID_PREFIX + str(self.future_tail_id)
        self.future_tail_id = (self.future_tail_id + 1) % self.CAPACITY
        return id

class QueueEntry:
    def __init__(self, dest, value=None):
        self.dest = dest
        self.value = value

    def __repr__(self):
        return 'QueueEntry(%r, %r)' % (self.dest, self.value)
