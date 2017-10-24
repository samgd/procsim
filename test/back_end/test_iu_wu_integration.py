from copy import deepcopy
import unittest

from procsim.back_end.integer_unit import IntegerUnit
from procsim.back_end.result import Result
from procsim.back_end.write_unit import WriteUnit
from procsim.instructions import Add
from procsim.register_file import RegisterFile
from procsim.memory import Memory

class TestIUWUIntegration(unittest.TestCase):

    def test_iu_wu_integration(self):
        """Ensure different operate and trigger orders have equal outputs.

        Separating the state computation from the state advancement means that
        the output should be deterministic regardless of which component each
        method is called on first. (Operate called on all first, followed by
        trigger)
        """
        traces = {'run_0': [], 'run_1': []}

        for run in traces:
            reg_file = RegisterFile(3, init_values={'r1': 2, 'r2': 3})
            write = WriteUnit(reg_file, Memory(100))
            integ = IntegerUnit(reg_file, write)
            integ.feed(Add('r0', 'r1', 'r2'))

            traces[run].append(deepcopy(reg_file))
            for _ in range(10):
                if run == 'run_0':
                    integ.operate()
                    write.operate()
                    integ.trigger()
                    write.trigger()
                else:
                    write.operate()
                    integ.operate()
                    write.trigger()
                    integ.trigger()
                traces[run].append(deepcopy(reg_file))

        self.assertEqual(traces['run_0'], traces['run_1'])
