import random
import unittest

from procsim.instructions import Add
from procsim.back_end.reservation_station import ReservationStation

class TestReservationStation(unittest.TestCase):

    def test_invalid_capacity(self):
        """Test exception thrown when initialized with invalid capacity."""
        for _ in range(100):
            invalid = random.randint(-1000, 0)
            with self.assertRaises(ValueError):
                ReservationStation(capacity=invalid)

    def test_feed_busy(self):
        """Test busy operation when feeding Instructions."""
        for capacity in [1, 5, 25, 200]:
            rs = ReservationStation(capacity=capacity)
            for _ in range(capacity):
                self.assertFalse(rs.busy(),
                                 'ReservationStation should not be busy after < capacity feeds')
                rs.feed(Add('r0', 'r1', 'r2'))
            self.assertTrue(rs.busy(),
                            'ReservationStation should be busy after capacity feeds')
            with self.assertRaises(AssertionError):
                rs.feed(Add('r1', 'r2', 'r3'))
