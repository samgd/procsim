import random
import unittest

from procsim.branch.branch_info import BranchInfo
from procsim.branch.static.always_taken import AlwaysTaken
from procsim.front_end.instructions.blth import Blth

class TestAlwaysTaken(unittest.TestCase):

    def test_never_taken(self):
        predictor = AlwaysTaken()

        for _ in range(100):
            pc = random.randint(1, 1000)
            imm = random.randint(1, 1000)
            blth = Blth('r1', 'r2', imm)
            self.assertEqual(predictor.predict(pc, str(blth)),
                             BranchInfo(True, imm, pc + 1, pc))
