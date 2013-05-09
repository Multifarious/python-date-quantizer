# datequant: Assorted Python date quantization functions.

```
>>> from datetime import date,datetime
>>> from datequant import *
>>> quarter(date(2013,5,3))
2
>>> week_num_2006_01_01(as_utc_datetime(datetime(2006,1,7,17,10)))
0
>>> week_num_2006_01_01(as_utc_datetime(datetime(2006,1,8,17,10)))
1
>>> hour_floor(datetime(2012,2,2,17,17,17))
datetime.datetime(2012, 2, 2, 17, 0)
>>> as_datetime(1367601023)
datetime.datetime(2013, 5, 3, 17, 10, 23, tzinfo=<UTC>)
>>> as_datetime(date.today())
datetime.datetime(2013, 5, 9, 0, 0)
>>> as_datetime(datetime.now())
datetime.datetime(2013, 5, 9, 15, 26, 50, 606995)
>>> as_utc_datetime(datetime.now())
datetime.datetime(2013, 5, 9, 15, 27, 5, 446303, tzinfo=<UTC>)
```

## Date Entities

Also provides script for generating date entities a CSV data for ingestion into a RDBMS. See `generate_dates.py`
