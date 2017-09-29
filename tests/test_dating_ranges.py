""" Unit tests for dating.ranges """
import unittest
from datetime import date, datetime
from itertools import islice
from random import shuffle

from arrow import Arrow, get as get_arrow
from dating.ranges import DateTimeRange


class TestDateTimeRangeWithArrows(unittest.TestCase):
    """ Testing the DateTimeRange class with Arrow objects """
    def setUp(self):
        self.now = Arrow.utcnow()
        self.start = self.now
        self.end = self.now.shift(days=15)
        self.before_start = self.now.shift(days=-1)
        self.after_end = self.end.shift(days=1)
        self.dtr = DateTimeRange(self.start, self.end)
        self.left_open_dtr = DateTimeRange(None, self.end)
        self.right_open_dtr = DateTimeRange(self.start, None)

    def test_str(self):
        expected_str = "[{} - {}]".format(self.start, self.end)
        self.assertEqual(str(self.dtr), expected_str)

    def test_arrow_properties(self):
        self.assertEqual(self.dtr.start_arrow, self.start)
        self.assertEqual(self.dtr.end_arrow, self.end)

    def test_datetime_properties(self):
        self.assertEqual(self.dtr.start_datetime, self.start.datetime)
        self.assertEqual(self.dtr.end_datetime, self.end.datetime)

    def test_date_properties(self):
        self.assertEqual(self.dtr.start_date, self.start.date())
        self.assertEqual(self.dtr.end_date, self.end.date())

    def test_string_constructor_with_datetimes(self):
        start_str = "2017-01-12T14:25:10"
        end_str = "2017-02-15T07:00:01"
        dtr1 = DateTimeRange.from_strings(start_str, end_str)
        self.assertEqual(dtr1.start_datetime, get_arrow(start_str))
        self.assertEqual(dtr1.end_datetime, get_arrow(end_str))

    def test_string_constructor_with_dates(self):
        dtr1 = DateTimeRange.from_strings("2017-01-12", "2017-02-15")
        self.assertEqual(dtr1.start_date, date(2017, 1, 12))
        self.assertEqual(dtr1.end_date, date(2017, 2, 15))

    def test_month_for_arrow(self):
        mdtr = DateTimeRange.month_for_arrow(Arrow(2017, 2, 14, 15, 30))
        self.assertEqual(mdtr.start_datetime, Arrow(2017, 2, 1).floor('day').datetime)
        self.assertEqual(mdtr.end_datetime, Arrow(2017, 2, 28).ceil('day').datetime)

    def test_month_for_datetime(self):
        mdtr = DateTimeRange.month_for_datetime(datetime(2017, 2, 14, 15, 30))
        self.assertEqual(mdtr.start_datetime, Arrow(2017, 2, 1).floor('day').datetime)
        self.assertEqual(mdtr.end_datetime, Arrow(2017, 2, 28).ceil('day').datetime)

    def test_dtr_membership(self):
        self.assertTrue(self.start in self.dtr)
        self.assertTrue(self.start.shift(days=1) in self.dtr)
        self.assertTrue(self.end in self.dtr)
        self.assertFalse(self.before_start in self.dtr)
        self.assertFalse(self.after_end in self.dtr)

    def test_open_dtr_membership(self):
        self.assertTrue(self.before_start in self.left_open_dtr)
        self.assertTrue(self.after_end in self.right_open_dtr)
        self.assertFalse(self.after_end in self.left_open_dtr)
        self.assertFalse(self.before_start in self.right_open_dtr)

    def test_is_well_defined(self):
        self.assertTrue(self.dtr.is_well_defined())
        self.assertFalse(self.left_open_dtr.is_well_defined())
        self.assertFalse(self.right_open_dtr.is_well_defined())

    def test_iterator(self):
        expected_dates = [self.start.shift(days=x) for x in range(16)]
        self.assertEqual(list(self.dtr), expected_dates)
        self.assertEqual(list(islice(self.right_open_dtr, 16)), expected_dates)

    def test_eq(self):
        dtr2 = DateTimeRange.from_datetimes(self.start.datetime, self.end.datetime)
        self.assertEqual(self.dtr, dtr2)

    def test_gt(self):
        dtr2 = DateTimeRange(self.before_start)
        self.assertTrue(self.dtr > dtr2)
        dtr3 = DateTimeRange(self.start.shift(days=2))
        self.assertTrue(dtr3 > self.dtr)

    def test_lt(self):
        dtr2 = DateTimeRange(self.before_start)
        self.assertTrue(dtr2 < self.dtr)
        dtr3 = DateTimeRange(self.start)
        self.assertTrue(self.dtr < dtr3)

    def test_gte(self):
        dtr2 = DateTimeRange(self.start, self.start.shift(days=12))
        self.assertTrue(self.dtr >= dtr2)

    def test_lte(self):
        dtr2 = DateTimeRange(self.start.shift(days=1), self.start.shift(days=15))
        self.assertTrue(self.dtr <= dtr2)

    def test_sort(self):
        dtr1 = DateTimeRange(self.before_start)
        dtr2 = DateTimeRange(self.start.shift(days=1), self.start.shift(days=15))
        ranges = [self.dtr, dtr2, dtr1, self.left_open_dtr, self.right_open_dtr]
        shuffle(ranges)
        self.assertEqual(sorted(ranges),
                         [self.left_open_dtr, dtr1, self.dtr, self.right_open_dtr, dtr2])
