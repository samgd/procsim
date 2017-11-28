import random
import unittest

from procsim.branch.branch_info import BranchInfo
from procsim.branch.dynamic.branch_history_table import BranchHistoryTable

class TestBranchHistoryTable(unittest.TestCase):

    def test_weak_taken_initialization(self):
        """Ensure BHT entries are initialized to weak taken."""
        n_entries = 128
        blth_str = 'blth r1 r2 100'

        for n_prediction_bits in [1, 2, 4, 16]:
            bht = BranchHistoryTable(n_entries, n_prediction_bits)

            for pc in range(n_entries):
                # Weakly taken, predict taken.
                branch_info = bht.predict(pc, blth_str)
                self.assertEqual(branch_info,
                                 BranchInfo(True, 100, pc + 1, pc))
                # Receive not taken so now weakly not taken, predict not taken.
                bht.receive(pc, False)
                branch_info = bht.predict(pc, blth_str)
                self.assertEqual(branch_info,
                                 BranchInfo(False, 100, pc + 1, pc))

    def test_saturating_counter(self):
        """Test that the internal counter saturates."""
        blth_str = 'blth r1 r2 100'
        exp_info = BranchInfo(False, 100, 1, 0)

        for n_prediction_bits in [1, 2, 4, 16]:
            bht = BranchHistoryTable(1, n_prediction_bits)

            # Set counter to strongly not taken. More than req. to catch underflow.
            for _ in range((2**n_prediction_bits) * 3):
                bht.receive(0, False)

            for _ in range(2**(n_prediction_bits - 1)):
                branch_info = bht.predict(0, blth_str)
                self.assertEqual(branch_info, exp_info,
                                 msg='BHT should take 2**(n - 1) receives to predict taken')
                bht.receive(0, True)

            branch_info = bht.predict(0, blth_str)
            exp_info.taken = True
            self.assertEqual(branch_info, exp_info,
                             msg='BHT should predict taken after 2**(n - 1) receives')

            # Set counter to strongly taken. More than req. to catch overflow.
            for _ in range((2**n_prediction_bits) * 3):
                bht.receive(0, True)

            for _ in range(2**(n_prediction_bits - 1)):
                branch_info = bht.predict(0, blth_str)
                self.assertEqual(branch_info, exp_info,
                                 msg='BHT should take 2**(n - 1) receives to predict not taken')
                bht.receive(0, False)

            branch_info = bht.predict(0, blth_str)
            exp_info.taken = False
            self.assertEqual(branch_info, exp_info,
                             msg='BHT should predict taken after 2**(n - 1) receives')
