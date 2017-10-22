from procsim.run.args import get_args

from procsim.back_end.branch_unit import BranchUnit
from procsim.back_end.integer_unit import IntegerUnit
from procsim.back_end.reservation_station import ReservationStation
from procsim.back_end.write_unit import WriteUnit
from procsim.clock import Clock
from procsim.front_end.decode import Decode
from procsim.front_end.fetch import Fetch
from procsim.register_file import RegisterFile

ARGS = get_args()

REGISTER_FILE = RegisterFile(ARGS.n_gpr_registers,
                             ARGS.gpr_prefix)

RES_STATION = ReservationStation()

DECODE = Decode(RES_STATION)
FETCH = Fetch(REGISTER_FILE, ARGS.FILE, DECODE, sequential=True)

WRITE_UNIT = WriteUnit(REGISTER_FILE, fetch=FETCH)
INTEGER_UNIT = IntegerUnit(REGISTER_FILE, WRITE_UNIT)
BRANCH_UNIT = BranchUnit(REGISTER_FILE, WRITE_UNIT, fetch=FETCH)

RES_STATION.register(INTEGER_UNIT)
RES_STATION.register(BRANCH_UNIT)

CLOCK = Clock()
CLOCK.register(RES_STATION)
CLOCK.register(DECODE)
CLOCK.register(FETCH)
CLOCK.register(WRITE_UNIT)
CLOCK.register(INTEGER_UNIT)
CLOCK.register(BRANCH_UNIT)

clock_ticks = 0
while True:
    print(str(clock_ticks) + ':\t',
          'r0:', REGISTER_FILE['r0'],
          'r1:', REGISTER_FILE['r1'],
          'r2:', REGISTER_FILE['r2'],
          'pc:', REGISTER_FILE['pc'])
    CLOCK.tick()
    clock_ticks += 1
    input()
