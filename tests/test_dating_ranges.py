import unittest
import pytz
from datetime import date, datetime, timedelta, time
from itertools import islice
from random import shuffle

from dating.ranges import DateRange, DateTimeRange


TODAY = date.today()
P1D = timedelta(days=1)
P15D = timedelta(days=15)
YESTERDAY = TODAY - P1D
TOMORROW = TODAY + P1D

DT_NOW = datetime.now()
DT_TOMORROW = datetime.combine(TOMORROW, DT_NOW.time())
DT_YESTERDAY = datetime.combine(YESTERDAY, DT_NOW.time())

UTC = pytz.utc

class TestDateTimeRange(unittest.TestCase):
    def setUp(self):
        self.start_datetime = DT_NOW
        self.end_datetime = DT_NOW + P15D
        self.before_start = DT_YESTERDAY
        self.after_end = self.end_datetime + P1D
        self.dtr = DateTimeRange(self.start_datetime, self.end_datetime)
        self.left_open_dtr = DateTimeRange(None, self.end_datetime)
        self.right_open_dtr = DateTimeRange(self.start_datetime, None)

    def test_str(self):
        dtr_str = str(self.dtr)
        expected_str = "({} - {})".format(UTC.localize(self.start_datetime), 
                                          UTC.localize(self.end_datetime))
        self.assertEqual(dtr_str, expected_str)

    def test_date_properties(self):
        self.assertEqual(self.dtr.start_date, self.start_datetime.date())
        self.assertEqual(self.dtr.end_date, self.end_datetime.date())

    def test_string_constructor(self):
        dtr1 = DateTimeRange.from_strings("2017-01-12T14:25:10", "2017-02-15T07:00:01")
        self.assertEqual(dtr1.start_datetime, datetime(2017, 1, 12, 14, 25, 10, 0, UTC))
        self.assertEqual(dtr1.end_datetime, datetime(2017, 2, 15, 7, 0, 1, 0, UTC))


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

    def test_open_dr_membership(self):
        self.assertTrue(self.before_start in self.left_open_dr)
        self.assertTrue(self.after_end in self.right_open_dr)
        self.assertFalse(self.after_end in self.left_open_dr)
        self.assertFalse(self.before_start in self.right_open_dr)

    def test_string_constructor(self):
        dr1 = DateRange.from_strings("2017-01-12", "2017-02-15")
        self.assertEqual(dr1.start_date, date(2017, 1, 12))
        self.assertEqual(dr1.end_date, date(2017, 2, 15))

    def test_str(self):
        dr_str = str(self.dr)
        expected_str = "({} - {})".format(self.start_date, self.end_date)
        self.assertEqual(dr_str, expected_str)

    def test_is_well_defined(self):
        self.assertTrue(self.dr.is_well_defined())
        self.assertFalse(self.left_open_dr.is_well_defined())
        self.assertFalse(self.right_open_dr.is_well_defined())

    def test_iterator(self):
        expected_dates = [UTC.localize(datetime.combine(self.start_date, time.min) + timedelta(days=x)) for x in range(16)]
        self.assertEqual(list(self.dr), expected_dates)
        self.assertEqual(list(islice(self.right_open_dr, 16)), expected_dates)

    def test_eq(self):
        dr2 = DateRange.from_strings(str(self.dr.start_date), str(self.dr.end_date))
        self.assertEqual(self.dr, dr2)

    def test_gt(self):
        dr2 = DateRange(YESTERDAY)
        self.assertTrue(self.dr > dr2)
        dr3 = DateRange(TODAY)
        self.assertTrue(dr3 > self.dr)

    def test_lt(self):
        dr2 = DateRange(YESTERDAY)
        self.assertTrue(dr2 < self.dr)
        dr3 = DateRange(TODAY)
        self.assertTrue(self.dr < dr3)
    
    def test_gte(self):
        dr2 = DateRange(TODAY, TODAY+timedelta(days=12))
        self.assertTrue(self.dr >= dr2)

    def test_lte(self):
        dr2 = DateRange(TOMORROW, TODAY+P15D)
        self.assertTrue(self.dr <= dr2)

    def test_sort(self):
        dr1 = DateRange(YESTERDAY)
        dr2 = DateRange(TOMORROW, TODAY+P15D)
        ranges = [self.dr, dr2, dr1, self.left_open_dr, self.right_open_dr]
        shuffle(ranges)
        self.assertEqual(sorted(ranges), [self.left_open_dr, dr1, self.dr, self.right_open_dr, dr2])
