from datetime import date, timedelta
import iso8601

class DateRange:
    start_date = None
    end_date = None

    def __init__(self, start_date=None, end_date=None):
        self.start_date = start_date
        self.end_date = end_date

    @classmethod
    def from_strings(cls, start_date_str=None, end_date_str=None):
        return cls(start_date=iso8601.parse_date(start_date_str) if start_date_str else None,
                   end_date=iso8601.parse_date(end_date_str) if end_date_str else None)

    def __str__(self):
        return "({} - {})".format(self.start_date, self.end_date)

    def __iter__(self):
        self._pointer = self.start_date
        self._step = timedelta(days=1)
        return self

    def _after_start(self, a_date):
        return (not self.start_date) or (a_date >= self.start_date)

    def _before_end(self, a_date):
        return (not self.end_date) or (a_date <= self.end_date)

    def __contains__(self, a_date):
        return self._after_start(a_date) and self._before_end(a_date)

    def __next__(self):
        if self._before_end(self._pointer):
            return_value = self._pointer
            self._pointer += self._step
            return return_value
        raise StopIteration()

    def is_well_defined(self):
        return self.start_date and self.end_date

    def __gt__(self, dt):
        return (not self.end_date) or dt > self.end_date

    def __gte__(self, dt):
        return (not self.end_date) or dt >= self.end_date

    def __lt__(self, dt):
        return (not self.start_date) or dt < self.start_date

    def __lte__(self, dt):
        return (not self.start_date) or dt <= self.start_date


class DateTimeRange(DateRange):

    @classmethod
    def from_strings(cls, start_date_str=None, end_date_str=None):
        return cls(start_date=iso8601.parse_datetime(start_date_str) if start_date_str else None,
                   end_date=iso8601.parse_datetime(end_date_str) if end_date_str else None)
