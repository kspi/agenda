import cache
import sys
from register import register_event
from datetime import timedelta, date
import requests
import requests.exceptions
from icalendar import Calendar, Event, prop

def simple(month, day, title, year=None):
    if year:
        @register_event
        def simple_fn(aday):
            if aday.month == month and aday.day == day:
                yield title.format(aday.year - year)
    else:
        @register_event
        def simple_fn(aday):
            if aday.month == month and aday.day == day:
                yield title

def birthday(month, day, name, year=None):
    if year:
        simple(month, day, "Gimtadienis: " + name + ", sukanka {}", year)
    else:
        simple(month, day, "Gimtadienis: " + name)

def from_ical_date(d):
    return prop.vDate.from_ical(d.to_ical().decode('utf-8'))

def icalendar(name, url):
    def fetch():
        response = requests.get(url)
        assert(response.status_code == 200)
        return response.text
    @register_event
    def icalendar_fn(day):
        body = cache.get("{}.ics".format(name), 60 * 12, fetch)
        if body is None:
            # Cache empty and update failed.
            return
        cal = Calendar.from_ical(body)
        for e in cal.walk():
            if isinstance(e, Event):
                title = e['SUMMARY']
                uid = e['UID']
                start = from_ical_date(e['DTSTART'])
                end = from_ical_date(e['DTEND'])
                if start == day:
                    yield "{}: {} ({})".format(name, title, uid)
