from datetime import date, timedelta
import iso8601

class DateRange:
    start_date = None
    end_date = None

    def __init__(self, start_date=None, end_date=None):
        self.start_date = start_date or date.min
        self.end_date = end_date or date.max

    @classmethod
    def from_strings(cls, start_date_str=None, end_date_str=None):
        return cls(start_date=iso8601.parse_date(start_date_str).date() if start_date_str else None,
                   end_date=iso8601.parse_date(end_date_str).date() if end_date_str else None)

    def __str__(self):
        return "({} - {})".format(self.start_date, self.end_date)

    def __iter__(self):
        self._pointer = self.start_date
        self._step = timedelta(days=1)
        return self

    def is_well_defined(self):
        return (self.start_date > date.min) and (self.end_date < date.max)

    def __contains__(self, a_date):
        return a_date >= self.start_date and a_date <= self.end_date

    def __next__(self):
        if self._pointer <= self.end_date:
            return_value = self._pointer
            self._pointer += self._step
            return return_value
        raise StopIteration()

    def __eq__(self, other):
        return ((self.start_date == other.start_date) and
                (self.end_date == other.end_date))

    def __lt__(self, other):
        return self.start_date < other.start_date

    def __le__(self, other):
        return (self.start_date <= other.start_date) and (self.end_date <= other.end_date)

    def __gt__(self, other):
        return self.start_date > other.start_date

    def __ge__(self, other):
        return (self.start_date >= other.start_date) and (self.end_date >= other.end_date)


class DateTimeRange(DateRange):

    @classmethod
    def from_strings(cls, start_date_str=None, end_date_str=None):
        return cls(start_date=iso8601.parse_date(start_date_str) if start_date_str else None,
                   end_date=iso8601.parse_date(end_date_str) if end_date_str else None)
