import unittest

from procsim.back_end.result import Result

class TestResult(unittest.TestCase):

    def test_result_equality(self):
        result = Result('r0', 10)

        none = Result('r1', 11)
        self.assertFalse(result == none, 'no attributes equal')

        val = Result('r2', 10)
        self.assertFalse(result == val, 'val equal but not dest')

        dest = Result('r0', 11)
        self.assertFalse(result == dest, 'dest equal but not val')

        val_dest = Result('r0', 10)
        self.assertTrue(result == val_dest, 'both attributes equal')
