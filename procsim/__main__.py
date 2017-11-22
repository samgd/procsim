import importlib
import sys

from procsim.run.args import get_args

from procsim.back_end.branch_unit import BranchUnit
from procsim.back_end.broadcast_bus import BroadcastBus
from procsim.back_end.integer_unit import IntegerUnit
from procsim.back_end.load_store_queue import LoadStoreQueue
from procsim.back_end.reorder_buffer import ReorderBuffer
from procsim.back_end.reservation_station import ReservationStation
from procsim.clock import Clock
from procsim.front_end.decode import Decode
from procsim.front_end.fetch import Fetch

args = get_args()

try:
    program = importlib.import_module(args.PROGRAM)
except:
    sys.exit('unable to load program %r' % args.PROGRAM)

# Create processor components.
clock = Clock()

register_file = program.REGISTER_FILE
memory = program.MEMORY

broadcast_bus = BroadcastBus()

branch_unit = BranchUnit(broadcast_bus)
integer_unit = IntegerUnit(broadcast_bus)

reservation_station = ReservationStation()
load_store_queue = LoadStoreQueue(memory, broadcast_bus)

reorder_buffer = ReorderBuffer(register_file,
                               reservation_station,
                               load_store_queue)

decode = Decode(reorder_buffer)
fetch = Fetch(register_file, program.PROGRAM, decode)

# Add additional connections.
broadcast_bus.subscribe(reservation_station)
broadcast_bus.subscribe(load_store_queue)
broadcast_bus.subscribe(reorder_buffer)

reservation_station.register(branch_unit)
reservation_station.register(integer_unit)

clock.register(branch_unit)
clock.register(integer_unit)
clock.register(reservation_station)
clock.register(load_store_queue)
clock.register(reorder_buffer)
clock.register(decode)
clock.register(fetch)

reorder_buffer.set_pipeline_flush_root(fetch)

while True:
    print(str(clock.n_ticks) + ':\t',
          'r0:', register_file['r0'],
          'r1:', register_file['r1'],
          'r2:', register_file['r2'],
          'r3:', register_file['r3'],
          'r4:', register_file['r4'],
          'r5:', register_file['r5'],
          'pc:', register_file['pc'], '\n',
          'memory:', memory.memory)
    clock.tick()
    input()
