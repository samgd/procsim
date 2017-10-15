import unittest

from procsim.register_file import RegisterFile
from procsim.back_end.result import Result
from procsim.back_end.write_unit import WriteUnit

class TestWriteUnit(unittest.TestCase):

    def setUp(self):
        init_values = {'r%d' % i: i for i in range(10)}
        self.reg_file = RegisterFile(10, init_values=init_values)

    def test_feed_write_delay(self):
        """Test write occurs after given write_delay."""
        result = Result('r0', 10)
        for write_delay in [1, 5, 10]:
            unit = WriteUnit(self.reg_file, write_delay)
            unit.feed(result)
            self.assertNotEqual(self.reg_file[result.dest], result.value,
                                'RegisterFile updated before write_delay')
            # Perform write_delay - 1 ticks.
            for _ in range(write_delay - 1):
                unit.tick()
                self.assertNotEqual(self.reg_file[result.dest], result.value,
                                    'RegisterFile updated before write_delay')
            # Call tick to trigger write.
            unit.tick()
            self.assertEqual(self.reg_file[result.dest], result.value,
                             'RegisterFile not updated after write_delay')
            # Reset RegisterFile.
            self.reg_file['r0'] = 0

    def test_feed_busy(self):
        """Test busy returns True after feed and False after write_delay."""
        result = Result('r0', 10)
        for write_delay in [1, 5, 10]:
            unit = WriteUnit(self.reg_file, write_delay)
            self.assertFalse(unit.busy(),
                             'WriteUnit busy after initialization')
            unit.feed(result)
            self.assertTrue(unit.busy(),
                            'WriteUnit not busy after being fed')
            for _ in range(write_delay - 1):
                unit.tick()
                self.assertTrue(unit.busy(),
                                'WriteUnit not busy before write_delay ticks')
            unit.tick()
            self.assertFalse(unit.busy(),
                             'WriteUnit busy after write_delay ticks')
