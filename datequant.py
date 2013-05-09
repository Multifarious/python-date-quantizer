from calendar import timegm
from datetime import datetime, time, timedelta
from pytz import utc

def as_unix_epoch(arg):
    """Convert provided date or datetime to unix epoch."""
    return timegm(arg.timetuple())

def as_datetime(arg):
    """Makes a datetime of the provided unix epoch, date, or datetime.
    Naive datetimes are left naive, aware datetimes are left in provided
    timezone."""
    if isinstance(arg,(int,float,long)):
        result = datetime.fromtimestamp(arg,utc)
    elif not isinstance(arg,datetime):
        result = datetime.combine(arg, time.min)
    else:
        result = arg
    return result

def as_utc_datetime(arg):
    """Makes a UTC datetime instance out of the provided unix epoch, date, or datetime.
    Naive datetimes are assumed to be UTC, timezone aware datetimes are properly
    converted."""
    dt = as_datetime(arg)
    if dt.tzinfo == utc:
        return dt
    elif dt.tzinfo is None:
        #Naive to aware conversion by assuming UTC
        return dt.replace(tzinfo=utc)
    else:
        #Aware to aware timezone conversion
        return dt.astimezone(utc)

#
# TODO: All these floor methods don't do DST conversions. E.g. if you year_floor a
# localized DST, you get a result that is still in DST. Best to use with either
# UTC or naive inputs for now.
#

def second_floor(to_quantize):
    """Converts provided input to UTC and truncates to a whole second."""
    return as_datetime(to_quantize).replace(microsecond=0)

def minute_floor(to_quantize):
    """Converts provided input to datetime and truncates to a whole minute."""
    return as_datetime(to_quantize).replace(second=0,microsecond=0)

def hour_floor(to_quantize):
    """Converts provided input to datetime and truncates to a whole hour."""
    return as_datetime(to_quantize).replace(minute=0,second=0,microsecond=0)

def day_floor(to_quantize):
    """Converts provided input to datetime and truncates to a whole day."""
    return as_datetime(to_quantize).replace(hour=0,minute=0,second=0,microsecond=0)

def week_floor(to_quantize):
    """Converts provided input to datetime and truncates to a whole week.
    Weeks start on Monday."""
    to_quantize = day_floor(to_quantize)
    return to_quantize - timedelta(days=to_quantize.weekday())

def sunday_based_day_of_week(day_of_week):
    """Convert a Monday-based day-of-week int to a Sunday-based one"""
    if day_of_week < 6:
        return day_of_week + 1
    else:
        return 0

def week_starting_sunday_floor(to_quantize):
    """Converts provided input to datetime and truncates to a whole week.
    Weeks start on Sunday."""
    to_quantize = day_floor(to_quantize)
    return to_quantize - timedelta(days=sunday_based_day_of_week(to_quantize.weekday()))

def month_floor(to_quantize):
    """Converts provided input to datetime and truncates to a whole month."""
    return as_datetime(to_quantize).replace(day=1,hour=0,minute=0,second=0,microsecond=0)

def quarter_floor(to_quantize):
    """Converts provided input to datetime and truncates to a whole quarter."""
    to_quantize = month_floor(to_quantize)
    new_month = to_quantize.month - (to_quantize.month % 3 - 1)
    return to_quantize.replace(month=new_month)

def year_floor(to_quantize):
    """Converts provided input to datetime and truncates to a whole year."""
    result = as_datetime(to_quantize).replace(month=1, day=1,hour=0,minute=0,second=0,microsecond=0)
    if result.tzinfo:
        result = result.astimezone(result.tzinfo)
    return result




WEEK_2006_01_01 = datetime(2006,1,1,tzinfo=utc)
def week_num_2006_01_01(to_quantize):
    """Converts provided input to datetime and calculates Sunday-based week number where week 0 starts Sunday, January 1st, 2006."""
    return (week_starting_sunday_floor(to_quantize) - WEEK_2006_01_01).days / 7

WEEK_2012_01_01 = datetime(2012,1,1,tzinfo=utc)
def week_num_2012_01_01(to_quantize):
    """Converts provided input to datetime and calculates Sunday-based week number where week 0 starts Sunday, January 1st, 2012."""
    return (week_starting_sunday_floor(to_quantize) - WEEK_2012_01_01).days / 7

def quarter(arg):
    """Converts provided input to datetime and calculates quarter number."""
    dt = as_datetime(arg)
    return ((dt.month - 1) / 3) + 1
