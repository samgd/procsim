from copy import copy

from procsim.back_end.instructions.conditional import Conditional
from procsim.back_end.instructions.branch import Branch
from procsim.back_end.instructions import load as back_end_load
from procsim.back_end.instructions import store as back_end_store
from procsim.back_end.instructions.integer_logical import IntegerLogical
from procsim.back_end.subscriber import Subscriber
from procsim.front_end.instructions import *
from procsim.pipeline_stage import PipelineStage

class ReorderBuffer(PipelineStage, Subscriber):
    """A ReorderBuffer that facilitates out-of-order instruction execution.

    Args:
        reg_file: RegisterFile to read values from.
        res_station: ReservationStation to feed backend Instructions to.
        load_store_queue: LoadStoreQueue to dispatch MemoryAccess Instructions
            to.
        capacity: Size of the buffer.  (Max Instructions that can be contained
            within the ReorderBuffer at any one time.)
        width: Maximum number of instructions to commit per cycle. Note that
            fewer instructions may be committed if the ReorderBuffer has no
            instructions in it's queue. (default 4)
    """

    REGISTER = 0
    MEMORY = 1

    def __init__(self, reg_file, res_station, load_store_queue, capacity=32, width=4):
        super().__init__()
        self.register_file = reg_file
        self.reservation_station = res_station
        self.load_store_queue = load_store_queue
        self.flush_root = None
        self.width = width

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

        self._init_lookup_tables()

        # Speculative execution flag.
        self.spec_exec = False

        # ROB needs to tell LSQ that an Instruction is no-longer speculative.
        # UID used to link Instructions across units.
        self.memory_uid = 0

    def _init_lookup_tables(self):
        self.translate_fn_lookup = {Add:   self._translate_arith_register,
                                    AddI:  self._translate_arith_imm,
                                    Sub:   self._translate_arith_register,
                                    SubI:  self._translate_arith_imm,
                                    Mul:   self._translate_arith_register,
                                    MulI:  self._translate_arith_imm,
                                    Load:  self._translate_memory_access,
                                    Store: self._translate_memory_access,
                                    Blth:  self._translate_conditional}

        self.operation_lookup = {Add:  lambda o1, o2: o1 + o2,
                                 AddI: lambda o1, o2: o1 + o2,
                                 Sub:  lambda o1, o2: o1 - o2,
                                 SubI: lambda o1, o2: o1 - o2,
                                 Mul:  lambda o1, o2: o1 * o2,
                                 MulI: lambda o1, o2: o1 * o2,
                                 Blth: lambda o1, o2: o1 < o2}

        self.type_lookup = {Add:   self.REGISTER,
                            AddI:  self.REGISTER,
                            Sub:   self.REGISTER,
                            SubI:  self.REGISTER,
                            Mul:   self.REGISTER,
                            MulI:  self.REGISTER,
                            Load:  self.MEMORY,
                            Store: self.MEMORY,
                            Blth:  self.REGISTER}

    def feed(self, front_end_ins):
        """Insert an Instruction into the ReorderBuffer.

        Args:
            front_end_ins: Frontend instruction to insert.
        """
        assert not self.full(front_end_ins), 'ReorderBuffer fed when full'

        # Translate to back_end Instruction.
        translate = self.translate_fn_lookup[type(front_end_ins)]
        back_end_ins = translate(front_end_ins)

        # Add a QueueEntry to ROB queue.
        if isinstance(back_end_ins, back_end_store.Store):
            queue_entry = QueueEntry(dest=None,
                                     value=None,
                                     done=True,
                                     typ=back_end_store.Store,
                                     spec_exec=self.spec_exec)
            queue_entry.uid = back_end_ins.uid
        elif isinstance(back_end_ins, back_end_load.Load):
            queue_entry = QueueEntry(dest=front_end_ins.rd,
                                     value=None,
                                     done=False,
                                     typ=back_end_load.Load,
                                     spec_exec=self.spec_exec)
            queue_entry.uid = back_end_ins.uid
        elif isinstance(back_end_ins, Conditional):
            # Conditional instructions should come with BranchInfo.
            queue_entry = QueueEntry(dest='pc',
                                     value=front_end_ins.branch_info,
                                     typ=Conditional,
                                     done=False,
                                     spec_exec=self.spec_exec)
            self.spec_exec = True
        else:
            queue_entry = QueueEntry(dest=front_end_ins.rd,
                                     value=None,
                                     typ=None,
                                     done=False,
                                     spec_exec=self.spec_exec)

        self.future_queue[back_end_ins.tag] = queue_entry

        # Feed to stage further down pipeline.
        typ = self.type_lookup[type(front_end_ins)]
        if typ == self.REGISTER:
            self.reservation_station.feed(back_end_ins)
        else:
            self.load_store_queue.feed(back_end_ins)

    def full(self, front_end_ins):
        """Return True if the ReorderBuffer is full.

        Args:
            front_end_ins: Check if ReorderBuffer can be fed this instruction.
                The ReorderBuffer requires a free slot in the
                ReservationStation if the Instruction only accesses Registers,
                or a free slot in the LoadStoreQueue if the Instruction
                accesses Memory.

        Returns:
            True if the ReorderBuffer is unable to be fed the instruction.
        """
        if self.future_tail_id is None:
            return True
        typ = self.type_lookup[type(front_end_ins)]
        if typ == self.REGISTER:
            return self.reservation_station.full()
        return self.load_store_queue.full()

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
            if n_commit == self.width:
                # Unable to commit any more this cycle.
                break

            id = self.ID_PREFIX + str(self.current_head_id)
            head = self.current_queue[id]
            if not head.done or head.spec_exec:
                # Value still being computed or still speculative.
                break

            # Process head entry.
            if head.typ == back_end_store.Store:
                self._process_store_entry(head)
            elif head.typ == Conditional:
                self._process_conditional_queue_entry(head)
            else:
                self._process_queue_entry(head)

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
        entry = self.future_queue[result.tag]
        if entry.typ != Conditional:
            entry.value = result.value
        else:
            # For QueueEntry value for Conditional instructions None indicates
            # correct prediction and an address indicates an incorrect
            # prediction.
            if entry.value.taken and result.value:
                # Predicted taken, actually taken.
                entry.value = None
            elif entry.value.taken and not result.value:
                # Predicted taken, not took.
                entry.value = entry.value.not_taken_addr
            elif not entry.value.taken and not result.value:
                # Predicted not taken, not took
                entry.value = None
            else:
                entry.value = entry.value.taken_addr
        entry.done = True

    def set_pipeline_flush_root(self, root):
        self.flush_root = root

    def flush(self):
        self.current_head_id = None
        self.current_tail_id = 0
        self.future_head_id = None
        self.future_tail_id = 0
        self.current_queue = {}
        self.future_queue = {}

        self.register_alias_table = {}

        self.spec_exec = False

        self.reservation_station.flush()
        self.load_store_queue.flush()

    def _translate_arith_register(self, front_end_ins):
        """Return a backend Instruction formed from a frontend instruction.

        This function will increment the ReorderBuffer's future queue tail
        pointer.

        Args:
            front_end_ins: Register-form arithmetic frontend instruction.

        Returns:
            IntegerLogical Instruction.
        """
        operand_1 = self._translate_operand(front_end_ins.r1)
        operand_2 = self._translate_operand(front_end_ins.r2)

        queue_id = self._get_queue_id()
        self.register_alias_table[front_end_ins.rd] = queue_id

        ins = IntegerLogical(queue_id,
                              self.operation_lookup[type(front_end_ins)],
                              operand_1,
                              operand_2)
        return ins

    def _translate_arith_imm(self, front_end_ins):
        """Return a backend Instruction formed from a frontend instruction.

        This function will increment the ReorderBuffer's future queue tail
        pointer.

        Args:
            front_end_ins: Immediate-form arithmetic frontend instruction.

        Returns:
            IntegerLogical Instruction.
        """
        operand_1 = self._translate_operand(front_end_ins.r1)
        operand_2 = front_end_ins.imm

        queue_id = self._get_queue_id()
        self.register_alias_table[front_end_ins.rd] = queue_id

        return IntegerLogical(queue_id,
                              self.operation_lookup[type(front_end_ins)],
                              operand_1,
                              operand_2)

    def _translate_memory_access(self, front_end_ins):
        """Return a backend Instruction formed from a frontend instruction.

        This function will increment the ReorderBuffer's future queue tail
        pointer if the resulting backend Instruction writes to a register.

        Args:
            front_end_ins: Frontend Load or Store instruction.

        Returns:
            MemoryAccess Instruction.
        """

        if isinstance(front_end_ins, Load):
            address = self._translate_operand(front_end_ins.r1)
            queue_id = self._get_queue_id()
            self.register_alias_table[front_end_ins.rd] = queue_id
            uid = self.memory_uid
            self.memory_uid += 1
            return back_end_load.Load(queue_id,
                                      address,
                                      uid,
                                      self.spec_exec)
        elif isinstance(front_end_ins, Store):
            address = self._translate_operand(front_end_ins.r1)
            value = self._translate_operand(front_end_ins.rs)
            uid = self.memory_uid
            self.memory_uid += 1
            queue_id = self._get_queue_id()
            return back_end_store.Store(queue_id,
                                        address,
                                        value,
                                        uid,
                                        self.spec_exec)
        raise ValueError('unknown MemoryAccess Instructions %r'
                         % type(front_end_ins).__name__)

    def _translate_conditional(self, front_end_ins):
        """Return a backend Instruction formed from a frontend instruction.

        This function will increment the ReorderBuffer's future queue tail
        pointer.

        Args:
            front_end_ins: Frontend Blth instruction.

        Returns:
            Conditional Instruction.
        """
        operand_1 = self._translate_operand(front_end_ins.r1)
        operand_2 = self._translate_operand(front_end_ins.r2)
        queue_id = self._get_queue_id()

        return Conditional(queue_id,
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
            rob_id = self.register_alias_table[register_name]
            entry = self.future_queue[rob_id]
            if entry.done:
                return entry.value
            return rob_id
        return self.register_file[register_name]

    def _process_store_entry(self, entry):
        id = self.ID_PREFIX + str(self.current_head_id)
        del self.future_queue[id]
        # ROB ID now free.
        if self.future_tail_id is None:
            self.future_tail_id = self.current_head_id
        self.current_head_id = (self.current_head_id + 1) % self.CAPACITY
        if self.current_head_id == self.current_tail_id:
            self.current_head_id = None

    def _process_queue_entry(self, entry):
        # Write value to RegisterFile and remove from future queue.
        self.register_file[entry.dest] = entry.value

        id = self.ID_PREFIX + str(self.current_head_id)

        del self.current_queue[id]
        del self.future_queue[id]
        # If RAT points to this ROB ID then we can remove the RAT entry as
        # the value is now in the RegisterFile.
        try:
            rat_id = self.register_alias_table[entry.dest]
            if rat_id == id:
                del self.register_alias_table[entry.dest]
        except KeyError:
            pass
        # ROB ID now free.
        if self.future_tail_id is None:
            self.future_tail_id = self.current_head_id
        self.current_head_id = (self.current_head_id + 1) % self.CAPACITY
        if self.current_head_id == self.current_tail_id:
            self.current_head_id = None

    def _process_conditional_queue_entry(self, entry):
        if entry.value is None:
            # Correct prediction.
            # All instructions in queue up to next conditional are no longer
            # being speculatively executed - set their flags to False.
            id = (self.current_head_id + 1) % self.CAPACITY
            # ROB spec_exec flag determines spec_exec attribute of future queue
            # entries. Set to False unless another conditional instruction is
            # in queue.
            self.spec_exec = False
            while id != self.current_head_id and id != self.current_tail_id:
                entry = self.future_queue[self.ID_PREFIX + str(id)]
                entry.spec_exec = False
                if entry.typ == back_end_store.Store or entry.typ == back_end_load.Load:
                    self.load_store_queue.speculative_execution_off(entry.uid)
                if entry.typ == Conditional:
                    self.spec_exec = True
                    break
                id = (id + 1) % self.CAPACITY

            # ROB ID now free.
            del self.current_queue[self.ID_PREFIX + str(self.current_head_id)]
            del self.future_queue[self.ID_PREFIX + str(self.current_head_id)]
            if self.future_tail_id is None:
                self.future_tail_id = self.current_head_id
            self.current_head_id = (self.current_head_id + 1) % self.CAPACITY
            if self.current_head_id == self.current_tail_id:
                self.current_head_id = None
        else:
            # Incorrect prediction.
            self.flush_root.flush()
            self.register_file['pc'] = entry.value

class QueueEntry:
    """An entry in a ReorderBuffer's circular queue.

    Attributes:
        dest: Target to store value in.
        value: Value to save to dest. None indicates that it is still to be
            computed by the processor. (default None)
        done: False if the QueueEntry is still waiting for the Instruction to
            be executed. (default False)
        typ: Type of Instruction that will produce a value for this QueueEntry.
            Allows for special handling of Result in receive.
        spec_exec: True if Instruction is being speculatively executed.
            (default False)
    """

    def __init__(self, dest, value=None, done=False, typ=None, spec_exec=False):
        self.dest = dest
        self.value = value
        self.done = done
        self.typ = typ
        self.spec_exec = spec_exec

    def __repr__(self):
        rep = 'QueueEntry(%r, %r, %r, %r, %r' % (self.dest, self.value, self.done, self.typ, self.spec_exec)
        if hasattr(self, 'uid'):
            rep += ', %r' % self.uid
        rep += ')'
        return rep
