import sys
from datetime import timedelta, date
import requests
import requests.exceptions
from icalendar import Calendar, Event, prop
from agenda import cache
from agenda.register import register_event


def once(year, month, day, title):
    @register_event
    def event_fn(aday):
        if aday.year == year and aday.month == month and aday.day == day:
            yield title

def yearly(month, day, title):
    @register_event
    def event_fn(aday):
        if aday.month == month and aday.day == day:
            yield title

def anniversary(year, month, day, title):
    @register_event
    def event_fn(aday):
        if aday.month == month and aday.day == day:
            yield title.format(aday.year - year)

def birthday(month, day, name, year=None):
    if year:
        anniversary(year, month, day, "Gimtadienis: " + name + ", sukanka {}")
    else:
        yearly(month, day, "Gimtadienis: " + name)


def from_ical_date(d):
    return prop.vDate.from_ical(d.to_ical().decode('utf-8'))

def icalendar(name, url):
    def fetch():
        try:
            response = requests.get(url, timeout=1)
            if response.status_code == 200:
                return response.text
            else:
                print("icalendar:{}: HTTP response not OK: {}".format(name, response.status_code))
                return None
        except requests.exceptions.RequestException as e:
            print("icalendar:{}: {}".format(name, e))
            return None
    body = cache.get("{}.ics".format(name), 60 * 12, fetch)
    if body is None:
        # Cache empty and update failed.
        return
    cal = Calendar.from_ical(body)
    @register_event
    def icalendar_fn(day):
        for e in cal.walk():
            if isinstance(e, Event):
                title = e['SUMMARY']
                url = e.get('URL', None) or e['UID']
                start = from_ical_date(e['DTSTART'])
                end = from_ical_date(e['DTEND'])
                if start == day:
                    yield "{}: {} ({})".format(name, title, url)
