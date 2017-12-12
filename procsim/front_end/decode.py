from copy import copy

from procsim.pipeline_stage import PipelineStage
import procsim.front_end.instructions as ins

class Decode(PipelineStage):
    """Decode decodes an instruction string to an instruction.

    Args:
        reorder_buffer: ReorderBuffer to feed results to.
        capacity: Size of the Decode unit's buffer. (default 4)
        width: Maximum number of instructions to decode per cycle. Note that
            fewer instructions may be decoded if the ReorderBuffer is full or
            the Decode unit has no buffered instructions to decode. (default 4)

    Attributes:
        DELAY: Number of clock cycles required to decode an instruction.
            (default 1)
    """

    def __init__(self, reorder_buffer, capacity=32, width=4):
        super().__init__()
        if capacity < 1:
            raise ValueError('capacity must be >= 1')
        self.reorder_buffer = reorder_buffer
        self.CAPACITY = capacity
        self.width = width
        self.DELAY = 1
        self.current_queue = []
        self.current_timer = 0
        self.future_queue = []
        self.future_timer = 0

    def feed(self, instruction):
        """Feed the Decode stage an Instruction string to decode.

        Args:
            instruction: A dictionary containing at least the instruction_str
            key with value being a string to decode.
        """
        assert len(self.future_queue) < self.CAPACITY,\
            'Decode fed when full'
        if len(self.future_queue) == 0:
            self.future_timer = max(0, self.DELAY - 1)
        self.future_queue.append(instruction)

    def full(self):
        """Return True if Decode is full.

        Returns:
            True if the Decode unit is unable to be fed.
        """
        return len(self.future_queue) == self.CAPACITY

    def operate(self):
        """Feed decoded instructions to the ReorderBuffer if possible."""
        if self.current_timer > 0:
            return
        n_issue = 0
        for instruct_str in self.current_queue:
            if n_issue == self.width:
                return
            instruct = _decode(instruct_str)
            if self.reorder_buffer.full(instruct):
                return
            self.reorder_buffer.feed(instruct)
            n_issue += 1

            del self.future_queue[0]

    def trigger(self):
        """Free up buffer space by removing issued instructions."""
        self.current_queue = self.future_queue
        self.current_timer = self.future_timer

        self.future_queue = copy(self.current_queue)
        self.future_timer = max(0, self.future_timer - 1)

    def flush(self):
        self.current_queue = []
        self.current_timer = 0

        self.future_queue = []
        self.future_timer = 0

        self.reorder_buffer.flush()

def _decode(instruction):
    """Return the instruction string decoded into an Instruction.

    Args:
        instruction: Dictionary containing instruction_str to decode.

    Returns:
        Instruction if instruction_str is valid.
    """
    # Very naive parser.
    gen_ins = {'add': lambda args: ins.Add(args[0], args[1], args[2]),
               'addi': lambda args: ins.AddI(args[0], args[1], int(args[2])),
               'sub': lambda args: ins.Sub(args[0], args[1], args[2]),
               'subi': lambda args: ins.SubI(args[0], args[1], int(args[2])),
               'mul': lambda args: ins.Mul(args[0], args[1], args[2]),
               'muli': lambda args: ins.MulI(args[0], args[1], int(args[2])),
               'ldr': lambda args: ins.Load(args[0], args[1]),
               'str': lambda args: ins.Store(args[0], args[1]),
               'j': lambda args: ins.Jump(int(args[0])),
               'blth': lambda args: ins.Blth(args[0], args[1], int(args[2])),
               'halt': lambda args: ins.Halt()}
    fields = instruction['instruction_str'].split(' ')
    try:
        front_end_ins = gen_ins[fields[0]](fields[1:])
        if fields[0] == 'blth':
            front_end_ins.branch_info = instruction['branch_info']
        return front_end_ins
    except:
        raise ValueError('unknown instruction %r' % instruction)
