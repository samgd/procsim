import procsim.instructions as ins
from procsim.pipeline_stage import PipelineStage

class Decode(PipelineStage):
    """Decode decodes an Instruction string to an Instruction.

    Args:
        reservation_station: ReservationStation to feed results to.

    Attributes:
        DELAY: Number of clock cycles required to decode an Instruction.
            (default 1)
    """

    def __init__(self, reservation_station):
        super().__init__()
        self.res_stat = reservation_station
        self.DELAY = 1
        self.current_inst = None
        self.current_timer = 0
        self.future_inst = None
        self.future_timer = 0

    def feed(self, instruction_str):
        """Feed the Decode stage an Instruction string to decode.

        Args:
            instruction_str: An Instruction string to decode.
        """
        assert self.future_inst is None, 'Decode fed when busy'
        self.future_inst = instruction_str
        self.future_timer = max(0, self.DELAY - 1)

    def busy(self):
        """Return True if the Decode stages future state is non-empty."""
        return self.future_inst is not None

    def operate(self):
        """Feed decoded Instruction to the ReservationStation if possible."""
        if self.current_inst and self.current_timer == 0 and not self.res_stat.busy():
            instruct = _decode(self.current_inst)
            self.res_stat.feed(instruct)

    def trigger(self):
        """Advance the state of the Decode stage and init a new future state."""
        # Update current state.
        self.current_inst = self.future_inst
        self.current_timer = self.future_timer
        # Initialize future state.
        if self.current_inst is None or self.current_timer == 0:
            self.future_inst = None
            self.future_timer = 0
        else:
            self.future_inst = self.current_inst
            self.future_timer = max(0, self.current_timer - 1)

def _decode(instruction_str):
    """Return the instruction string decoded into an Instruction.

    Args:
        instruction_str: Instruction to decode.

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
               'blth': lambda args: ins.Blth(args[0], args[1], int(args[2]))}
    fields = instruction_str.split(' ')
    try:
        return gen_ins[fields[0]](fields[1:])
    except:
        raise ValueError('unknown instruction %r' % instruction_str)
