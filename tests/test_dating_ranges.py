import unittest
from datetime import date, datetime, timedelta

from dating.ranges import DateRange

TODAY = date.today()
P1D = timedelta(days=1)
P15D = timedelta(days=15)
YESTERDAY = TODAY - P1D
TOMORROW = TODAY + P1D

class TestDateRange(unittest.TestCase):
    def setUp(self):
        self.start_date = TODAY
        self.end_date = TODAY + P15D
        self.before_start = YESTERDAY
        self.after_end = self.end_date + P1D
        self.dr = DateRange(self.start_date, self.end_date)
        self.left_open_dr = DateRange(None, self.end_date)
        self.right_open_dr = DateRange(self.start_date, None)

    def test_dr_constructor(self):
        self.assertEqual(self.dr.start_date, self.start_date)
        self.assertEqual(self.dr.end_date, self.end_date)

    def test_dr_membership(self):
        self.assertTrue(self.start_date in self.dr)
        self.assertTrue(self.start_date + P1D in self.dr)
        self.assertTrue(self.end_date in self.dr)
        self.assertFalse(self.before_start in self.dr)
        self.assertFalse(self.after_end in self.dr)
