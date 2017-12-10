import importlib
import matplotlib.pyplot as plt
import sys

from procsim.back_end.branch_unit import BranchUnit
from procsim.back_end.broadcast_bus import BroadcastBus
from procsim.back_end.integer_unit import IntegerUnit
from procsim.back_end.load_store_queue import LoadStoreQueue
from procsim.back_end.reorder_buffer import ReorderBuffer
from procsim.back_end.reservation_station import ReservationStation
from procsim.branch.dynamic.branch_history_table import BranchHistoryTable
from procsim.branch.static.always_taken import AlwaysTaken
from procsim.branch.static.back_taken_forward_not import BackTakenForwardNot
from procsim.branch.static.never_taken import NeverTaken
from procsim.clock import Clock
from procsim.end_of_program import EndOfProgram
from procsim.front_end.decode import Decode
from procsim.front_end.fetch import Fetch
from procsim.run.args import get_args

args = get_args()

try:
    program = importlib.import_module(args.PROGRAM)
except Exception as err:
    sys.exit('unable to load program %r, %r' % (args.PROGRAM, err))

# Create processor components.
clock = Clock()

register_file = program.REGISTER_FILE

memory = program.MEMORY

broadcast_bus = BroadcastBus()

branch_unit = BranchUnit(broadcast_bus)

integer_units = [IntegerUnit(broadcast_bus)
                 for _ in range(args.n_integer_units)]

reservation_station = ReservationStation(capacity=args.capacity,
                                         width=args.superscalar_width)

load_store_queue = LoadStoreQueue(memory,
                                  broadcast_bus,
                                  capacity=args.capacity,
                                  data_forwarding=True)

if args.always_taken:
    branch_predictor = AlwaysTaken()
elif args.never_taken:
    branch_predictor = NeverTaken()
elif args.back_taken_forward_not:
    branch_predictor = BackTakenForwardNot()
else:
    branch_predictor = BranchHistoryTable(n_entries=2**8, n_prediction_bits=2)

reorder_buffer = ReorderBuffer(register_file,
                               reservation_station,
                               load_store_queue,
                               branch_predictor=branch_predictor,
                               capacity=args.capacity,
                               width=args.superscalar_width)

decode = Decode(reorder_buffer,
                capacity=args.capacity,
                width=args.superscalar_width)
fetch = Fetch(register_file,
              program.PROGRAM,
              decode,
              branch_predictor,
              width=args.superscalar_width)

# Add additional connections.
broadcast_bus.subscribe(reservation_station)
broadcast_bus.subscribe(load_store_queue)
broadcast_bus.subscribe(reorder_buffer)

reservation_station.register(branch_unit)
for integer_unit in integer_units:
    reservation_station.register(integer_unit)

clock.register(branch_unit)
for integer_unit in integer_units:
    clock.register(integer_unit)
clock.register(reservation_station)
clock.register(load_store_queue)
clock.register(reorder_buffer)
clock.register(decode)
clock.register(fetch)

reorder_buffer.set_pipeline_flush_root(fetch)

if args.plot:
    cycles = []
    ins_per_cycle = []
    plt.ion()
    graph = plt.plot(cycles, ins_per_cycle)[0]
    plt.ylim(0, args.superscalar_width)
    plt.xlabel('Cycles')
    plt.ylabel('Instructions/Cycle')
    plt.title('Average Instruction Throughput')

try:
    while True:
        out = str(clock.n_ticks) + ':\t' + program.console_output()

        if args.step_execution:
            input(out)
        else:
            print(out)

        # Update graph.
        if args.plot:
            cycles.append(clock.n_ticks)
            ins_per_cycle.append(reorder_buffer.n_committed / max(1, clock.n_ticks))
            graph.set_xdata(cycles)
            graph.set_ydata(ins_per_cycle)
            plt.xlim(0, clock.n_ticks)
            plt.draw()
            plt.pause(0.01)

        clock.tick()
except EndOfProgram:
    print('end:\t' + program.console_output())
    rob = reorder_buffer
    print('Instructions Executed: %d' % rob.n_committed)
    print('Cycles: %d' % clock.n_ticks)
    print('Instructions/Cycle: %.2f' % (rob.n_committed / clock.n_ticks))
    accuracy = max(1, rob.n_branch_correct) / max(1, (rob.n_branch_correct + rob.n_branch_incorrect))
    print('Branch Prediction Accuracy: %.2f' % accuracy)
    input('Exit?')
