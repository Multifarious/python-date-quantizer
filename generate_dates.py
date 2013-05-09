#!/usr/bin/env python
from datetime import datetime, timedelta
from datequant import as_unix_epoch, quarter, week_num_2006_01_01
from pytz import timezone, utc

TIMEZONES = [utc, timezone('EST5EDT'), timezone('PST8PDT')]
START = datetime(2006,1,1,tzinfo=utc)
END = datetime(2034,1,1,tzinfo=utc)

"""Generates dates.csv of date entities from START to END. Columsn are:
date_id (which is the top-of-the-hour unix epoch),
for each of TIMEZONES:
    year,month,day,hour,
    quarter (1-based),
    day of year (1-based),
    day of week (Monday-starting 0-based),
    absolute week (0-based Sunday-starting weeks starting Sunday 2006-01-01),
    ISO8061 year and week numbers (see http://www.staff.science.uu.nl/~gent0113/calendar/isocalendar.htm)
"""

def flatten(l):
    "Performs one level of flattening."
    return [item for sublist in l for item in sublist]

def cols_for_timezone(a_timestamp,tz):
    t = a_timestamp.astimezone(tz)
    timetuple = t.timetuple()
    isocalendar = t.isocalendar()
    return [
        t.year,
        t.month,
        t.day,
        t.hour,
        quarter(t),
        timetuple.tm_yday,
        timetuple.tm_wday,
        week_num_2006_01_01(t),
        isocalendar[0],
        isocalendar[1],
    ]

f = open('dates.csv', 'w')
t = START
one_hour = timedelta(hours=1)
while t < END:
    f.write(','.join(
        [str(x) for x in
            [as_unix_epoch(t)] +
            flatten( [cols_for_timezone(t, tz) for tz in TIMEZONES] )
        ]
    ))
    f.write('\n')
    t = t + one_hour
f.close()
