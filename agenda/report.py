from datetime import date, datetime, timedelta
import icalendar
import sys
from agenda.register import day_events


def datespan(start, end, delta=timedelta(days=1)):
    cur = start
    while cur < end:
        yield cur
        cur += delta


def ical(days, file=sys.stdout.buffer):
    today = date.today()
    prevday = today
    calendar = icalendar.Calendar()
    for day in datespan(today, today + timedelta(days=days)):
        events = list(day_events(day))
        for name in events:
            event = icalendar.Event()
            event.add('SUMMARY', name)
            event.add('DTSTART', day)
            event.add('DTEND', day)
            calendar.add_component(event)
    file.write(calendar.to_ical())


def text(days, file=sys.stdout):
    today = date.today()
    prevday = today
    for day in datespan(today, today + timedelta(days=days)):
        events = list(day_events(day))
        if events:
            print(day.strftime("%F %A"), file=file)
            for event in events:
                print(event, file=file)
            print(file=file)
