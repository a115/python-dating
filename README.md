# python-dating

A Python 3 library for handling date ranges and time periods in a business context, based on Arrow. 

Install with:

    $ pip install dating

## DateTimeRange

The `DateTimeRange` class defines a range between two points in time. To use:

    from dating.ranges import DateTimeRange

    date_range = DateTimeRange.from_strings('2017-01-15', '2017-03-15')

or

    date_time_range = DateTimeRange.from_strings('2017-01-15T10:25:00', '2017-01-16T07:30:00')


