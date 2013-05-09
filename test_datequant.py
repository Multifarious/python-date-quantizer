#!/usr/bin/env python
from calendar import timegm
from datequant import *
from datetime import date,datetime
from pytz import timezone, utc
import unittest

class TestDateQuant(unittest.TestCase):
    date1 = datetime(2013,5,3,17,10,23,123,utc)
    pst8pdt = timezone('PST8PDT')
    date2 = pst8pdt.localize(datetime(2013,5,3,17,10,23,123)) # midnight May 4th in UTC

    def setUp(self):
        pass

    def test_as_unix_epoch(self):
        self.assertEqual(1367601023, as_unix_epoch(self.date1))
        self.assertEqual(1367601023, as_unix_epoch(self.date2))

    def test_as_utc_datetime(self):
        self.assertEqual(self.date1, as_utc_datetime(self.date1))
        self.assertEqual(datetime(2013,5,4,0,10,23,123,utc), as_utc_datetime(self.date2))

    def test_from_unix_time(self):
        for f in [second_floor, minute_floor, hour_floor, day_floor, week_floor, week_starting_sunday_floor, month_floor, year_floor]:
            self.assertEqual(f(self.date1), f(1367601023))

    def test_idempotency(self):
        for f in [second_floor, minute_floor, hour_floor, day_floor, week_floor, week_starting_sunday_floor, month_floor, year_floor]:
            self.assertEqual(f(self.date1), f(f(self.date1)))

    def test_second_floor(self):
        self.assertEqual(datetime(2013,5,3,17,10,23,tzinfo=utc), second_floor(self.date1))
        self.assertEqual(self.pst8pdt.localize(datetime(2013,5,3,17,10,23)), second_floor(self.date2))

    def test_minute_floor(self):
        self.assertEqual(datetime(2013,5,3,17,10,tzinfo=utc), minute_floor(self.date1))
        self.assertEqual(self.pst8pdt.localize(datetime(2013,5,3,17,10)), minute_floor(self.date2))

    def test_hour_floor(self):
        self.assertEqual(datetime(2013,5,3,17,tzinfo=utc), hour_floor(self.date1))
        self.assertEqual(self.pst8pdt.localize(datetime(2013,5,3,17)), hour_floor(self.date2))

    def test_day_floor(self):
        self.assertEqual(datetime(2013,5,3,tzinfo=utc), day_floor(self.date1))
        self.assertEqual(self.pst8pdt.localize(datetime(2013,5,3)), day_floor(self.date2))

    def test_week_floor(self):
        self.assertEqual(datetime(2013,4,29,tzinfo=utc), week_floor(self.date1))
        self.assertEqual(self.pst8pdt.localize(datetime(2013,4,29)), week_floor(self.date2))

    def test_week_starting_sunday_floor(self):
        self.assertEqual(datetime(2013,4,28,tzinfo=utc), week_starting_sunday_floor(self.date1))
        self.assertEqual(self.pst8pdt.localize(datetime(2013,4,28)), week_starting_sunday_floor(self.date2))

    def test_month_floor(self):
        self.assertEqual(datetime(2013,5,1,tzinfo=utc), month_floor(self.date1))
        self.assertEqual(self.pst8pdt.localize(datetime(2013,5,1)), month_floor(self.date2))

    def test_quarters(self):
        self.assertEqual(datetime(2013,4,1,tzinfo=utc), quarter_floor(self.date1))
        self.assertEqual(datetime(2013,1,1), quarter_floor(date(2013,1,1)))
        self.assertEqual(2, quarter(self.date1))
        self.assertEqual(1, quarter(date(2013,1,1)))

    def test_year_floor(self):
        self.assertEqual(datetime(2013,1,1,tzinfo=utc), year_floor(self.date1))
        # TODO: broken due to result still being in DST self.assertEqual(self.pst8pdt.localize(datetime(2013,1,1)), year_floor(self.date2))

    def test_week_num_2006_01_01(self):
        self.assertEqual(0, week_num_2006_01_01(datetime(2006,1,7,17,10,23,123,utc)))
        self.assertEqual(1, week_num_2006_01_01(datetime(2006,1,8,17,10,23,123,utc)))
        self.assertEqual(-1, week_num_2006_01_01(datetime(2005,12,28,17,10,23,123,utc)))
        self.assertEqual(382, week_num_2006_01_01(self.date1))

    def test_week_num_2012_01_01(self):
        self.assertEqual(0, week_num_2012_01_01(datetime(2012,1,7,17,10,23,123,utc)))
        self.assertEqual(1, week_num_2012_01_01(datetime(2012,1,8,17,10,23,123,utc)))
        self.assertEqual(-1, week_num_2012_01_01(datetime(2011,12,28,17,10,23,123,utc)))
        self.assertEqual(69, week_num_2012_01_01(self.date1))


if __name__ == '__main__':
    unittest.main()
