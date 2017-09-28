from datetime import date, datetime, time, timedelta
import calendar

import iso8601
import pytz


class DateTimeRange:
    def __init__(self, start=None, end=None, timezone=None):
        """ Initialise a new DateTimeRange from the given start and end datetime objects. 
        Ensure that the start and end datetimes are timezone-aware (use UTC by default). 
        If timezone is passed, localise start and end datetimes to that zone. """

        self._start_datetime = start or datetime.min
        self._end_datetime = end or datetime.max
        self.timezone = timezone or self._start_datetime.tzinfo or self._end_datetime.tzinfo or pytz.utc
        if self.timezone != self._start_datetime.tzinfo:
            self._start_datetime = self.timezone.localize(self._start_datetime)
        if self.timezone != self._end_datetime.tzinfo:
            self._end_datetime = self.timezone.localize(self._end_datetime)

    @classmethod
    def from_strings(cls, start_datetime_str=None, end_datetime_str=None):
        return cls(start=iso8601.parse_date(start_datetime_str) if start_datetime_str else None,
                   end=iso8601.parse_date(end_datetime_str) if end_datetime_str else None)

    @classmethod
    def month_for(cls, a_datetime):
        month_range = calendar.monthrange(a_datetime.year, a_datetime.month)
        month_start = datetime.combine(date(a_datetime.year, a_datetime.month, 1), a_datetime.time())
        month_end = datetime.combine(date(a_datetime.year, a_datetime.month, month_range[1]), a_datetime.time())
        return cls(start=month_start, end=month_end, timezone=a_datetime.tzinfo)

    @property
    def start_datetime(self):
        return self._start_datetime

    @property
    def end_datetime(self):
        return self._end_datetime

    @property
    def start_date(self):
        return self._start_datetime.date()

    @property
    def end_date(self):
        return self._end_datetime.date()

    def __str__(self):
        return "({} - {})".format(self._start_datetime, self._end_datetime)

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        self._pointer = self._start_datetime
        self._step = timedelta(days=1)
        return self

    def is_well_defined(self):
        return ((self._start_datetime > self.timezone.localize(datetime.min)) and 
                (self._end_datetime < self.timezone.localize(datetime.max)))

    def __contains__(self, a_datetime):
        return a_datetime >= self._start_datetime and a_datetime <= self._end_datetime

    def __next__(self):
        if self._pointer <= self._end_datetime:
            return_value = self._pointer
            self._pointer += self._step
            return return_value
        raise StopIteration()

    def __eq__(self, other):
        return ((self._start_datetime == other.start_datetime) and
                (self._end_datetime == other.end_datetime))

    def __lt__(self, other):
        return ((self._start_datetime < other.start_datetime) or 
                ((self._start_datetime == other.start_datetime) and (self._end_datetime < other.end_datetime)))

    def __le__(self, other):
        return (self._start_datetime <= other.start_datetime) and (self._end_datetime <= other.end_datetime)

    def __gt__(self, other):
        return ((self._start_datetime > other.start_datetime) or 
                (self._start_datetime == other.start_datetime) and (self._end_datetime > other.end_datetime))

    def __ge__(self, other):
        return (self._start_datetime >= other.start_datetime) and (self._end_datetime >= other.end_datetime)


class DateRange(DateTimeRange):

    def __init__(self, start=None, end=None, timezone=None):
        start_datetime = datetime.combine(start or date.min, time.min)
        end_datetime = datetime.combine(end or date.max, time.max)
        super().__init__(start=start_datetime, end=end_datetime, timezone=timezone)

    @classmethod
    def from_strings(cls, start_date_str=None, end_date_str=None):
        return cls(start=iso8601.parse_date(start_date_str).date() if start_date_str else None,
                   end=iso8601.parse_date(end_date_str).date() if end_date_str else None)

    def __str__(self):
        return "({} - {})".format(self.start_date, self.end_date)

    def __contains__(self, a_date):
        return a_date >= self.start_date and a_date <= self.end_date

