from datetime import date, datetime, timedelta
import icalendar
import sys
from agenda.register import day_events
import re


def datespan(start, end, delta=timedelta(days=1)):
    cur = start
    while cur < end:
        yield cur
        cur += delta


def tag_filter(events, tags):
    trs = [re.compile(r'{}\b'.format(re.escape(t))) for t in tags]
    for e in events:
        if all(tr.search(e) for tr in trs):
            yield e

def ical(days, tags=[], file=sys.stdout.buffer):
    today = date.today()
    prevday = today
    calendar = icalendar.Calendar()
    for day in datespan(today, today + timedelta(days=days)):
        for name in tag_filter(day_events(day), tags):
            event = icalendar.Event()
            event.add('SUMMARY', name)
            event.add('DTSTART', day)
            event.add('DTEND', day)
            calendar.add_component(event)
    file.write(calendar.to_ical())


def agenda(days, tags=[], file=sys.stdout, color=False):
    today = date.today()
    prevday = today
    for day in datespan(today, today + timedelta(days=days)):
        events = list(tag_filter(day_events(day), tags))
        if events:
            if color:
                print("\x1b[34m{:%F %A}\x1b[0m".format(day), file=file)
            else:
                print("{:%F %A}".format(day), file=file)
            for event in events:
                print(event, file=file)
            print(file=file)


def txt(days, tags=[], file=sys.stdout, color=False):
    today = date.today()
    prevday = today
    for day in datespan(today, today + timedelta(days=days)):
        for event in tag_filter(day_events(day), tags):
            print("{:%F} {}".format(day, event), file=file)
