#!/usr/bin/env python3
from datetime import date, datetime, timedelta
from dateutil.parser import parse
from dateutil.tz import tzlocal, tzutc
import requests
import icalendar
from register import day_events
import events
import locale
import sys

def datespan(start, end, delta=timedelta(days=1)):
    cur = start
    while cur < end:
        yield cur
        cur += delta

def main():
    if len(sys.argv) == 2:
        days = int(sys.argv[1])
    else:
        days = 62
    locale.setlocale(locale.LC_TIME, "lt_LT.utf8")
    today = date.today()
    prevday = today
    for day in datespan(today, today + timedelta(days=days)):
        events = list(day_events(day))
        if events:
            print(day.strftime("%F %A"))
            for event in events:
                print(event)
            print()

if __name__ == '__main__':
    main()
