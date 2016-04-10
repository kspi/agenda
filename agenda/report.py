from datetime import date, datetime, timedelta
import icalendar
import sys
from agenda import events

def ical(days, tags=[], file=sys.stdout.buffer):
    today = date.today()
    calendar = icalendar.Calendar()
    for day, name in events.between(today, today + timedelta(days=days), tags=tags):
        event = icalendar.Event()
        event.add('SUMMARY', name)
        event.add('DTSTART', day)
        event.add('DTEND', day)
        calendar.add_component(event)
    file.write(calendar.to_ical())


def agenda(days, tags=[], file=sys.stdout, color=False):
    today = date.today()
    prevday = None
    for day, name in events.between(today, today + timedelta(days=days), tags=tags):
        if day != prevday:
            if prevday is not None:
                print(file=file)
            if color:
                print("\x1b[34m{:%F %A}\x1b[0m".format(day), file=file)
            else:
                print("{:%F %A}".format(day), file=file)
            prevday = day
        print(name, file=file)


def txt(days, tags=[], file=sys.stdout, color=False):
    today = date.today()
    for day, name in events.between(today, today + timedelta(days=days), tags=tags):
        print("{:%F} {}".format(day, name), file=file)
