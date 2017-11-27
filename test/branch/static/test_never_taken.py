import random
import unittest

from procsim.branch.static.never_taken import NeverTaken

class TestNeverTaken(unittest.TestCase):

    def test_never_taken(self):
        predictor = NeverTaken()

        for i in range(100):
            pc = random.randint(1, 1000)
            self.assertEqual(predictor.predict(pc), pc + 1)
