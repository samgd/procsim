import importlib
import sys

from procsim.run.args import get_args

from procsim.back_end.branch_unit import BranchUnit
from procsim.back_end.integer_unit import IntegerUnit
from procsim.back_end.reservation_station import ReservationStation
from procsim.back_end.load_store_unit import LoadStoreUnit
from procsim.back_end.write_unit import WriteUnit
from procsim.clock import Clock
from procsim.front_end.decode import Decode
from procsim.front_end.fetch import Fetch

args = get_args()

try:
    program = importlib.import_module(args.PROGRAM)
except:
    sys.exit('unable to load program %r' % args.PROGRAM)

register_file = program.REGISTER_FILE
memory = program.MEMORY

res_station = ReservationStation()

decode = Decode(res_station)
fetch = Fetch(register_file, program.PROGRAM, decode, sequential=True)

write_unit = WriteUnit(register_file, memory, fetch=fetch)
integer_unit = IntegerUnit(register_file, write_unit)
branch_unit = BranchUnit(register_file, write_unit, fetch=fetch)
load_store_unit = LoadStoreUnit(register_file, memory, write_unit)

res_station.register(integer_unit)
res_station.register(branch_unit)
res_station.register(load_store_unit)

clock = Clock()
clock.register(res_station)
clock.register(decode)
clock.register(fetch)
clock.register(write_unit)
clock.register(integer_unit)
clock.register(branch_unit)
clock.register(load_store_unit)

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
