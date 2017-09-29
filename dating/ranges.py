""" Define a range class to represent data and operations between two points in time. """
from arrow import Arrow, get as get_arrow

class DateTimeRange:
    """ A range class representing data and operations between two points in time. """

    def __init__(self, start=None, end=None):
        """ Initialise a new DateTimeRange from the given start and end Arrow objects.  """
        self._start_arrow = start or Arrow.min
        self._end_arrow = end or Arrow.max
        self._pointer = None

    @classmethod
    def from_strings(cls, start_str=None, end_str=None):
        """ Initialise a new DateTimeRange from the given start and end datetime strings.  """
        return cls(start=get_arrow(start_str) if start_str else None,
                   end=get_arrow(end_str) if end_str else None)

    @classmethod
    def from_datetimes(cls, start_datetime, end_datetime):
        """ Initialise a new DateTimeRange from the given start and end datetime objects.  """
        return cls(start=Arrow.fromdatetime(start_datetime) if start_datetime else None,
                   end=Arrow.fromdatetime(end_datetime) if end_datetime else None)

    @classmethod
    def month_for_arrow(cls, an_arrow):
        """ Return the start and end of the month, in which the Arrow object belongs. """
        return cls(*an_arrow.span('month'))

    @classmethod
    def month_for_datetime(cls, a_datetime):
        """ Return the start and end of the month, in which the datetime object belongs. """
        return cls.month_for_arrow(Arrow.fromdatetime(a_datetime))

    @property
    def start_arrow(self):
        return self._start_arrow

    @property
    def end_arrow(self):
        return self._end_arrow

    @property
    def start_datetime(self):
        return self._start_arrow.datetime

    @property
    def end_datetime(self):
        return self._end_arrow.datetime

    @property
    def start_date(self):
        return self._start_arrow.date()

    @property
    def end_date(self):
        return self._end_arrow.date()

    def __str__(self):
        return "[{} - {}]".format(self._start_arrow, self._end_arrow)

    def __repr__(self):
        return self.__str__()

    def is_well_defined(self):
        return ((self._start_arrow > Arrow.min) and
                (self._end_arrow < Arrow.max))

    def __contains__(self, a_datetime):
        return a_datetime >= self._start_arrow and a_datetime <= self._end_arrow

    def __iter__(self):
        self._pointer = self._start_arrow
        return self

    def __next__(self):
        if self._pointer <= self._end_arrow:
            ret = self._pointer
            self._pointer = self._pointer.shift(days=1)
            return ret
        raise StopIteration

    def __eq__(self, other):
        return ((self._start_arrow == other.start_arrow) and
                (self._end_arrow == other.end_arrow))

    def __lt__(self, other):
        return ((self._start_arrow < other.start_arrow) or
                ((self._start_arrow == other.start_arrow) and (self._end_arrow < other.end_arrow)))

    def __le__(self, other):
        return (self._start_arrow <= other.start_arrow) and (self._end_arrow <= other.end_arrow)

    def __gt__(self, other):
        return ((self._start_arrow > other.start_arrow) or
                (self._start_arrow == other.start_arrow) and (self._end_arrow > other.end_arrow))

    def __ge__(self, other):
        return (self._start_arrow >= other.start_arrow) and (self._end_arrow >= other.end_arrow)
