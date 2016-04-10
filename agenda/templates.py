import sys
from datetime import timedelta, date, datetime
import urllib.request
import urllib.error
from icalendar import Calendar, Event, prop
from caldav import DAVClient
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


def icalendar_data(name, data):
    cal = Calendar.from_ical(data)
    @register_event
    def icalendar_fn(day):
        for e in cal.walk():
            if isinstance(e, Event):
                title = e['SUMMARY']
                url = e.get('URL', None)
                start = e['DTSTART'].dt
                if isinstance(start, datetime):
                    startdate = start.date()
                    starttime = start
                else:
                    startdate = start
                    starttime = None
                if startdate == day:
                    event = "{}: {}".format(name, title)
                    if starttime:
                        if starttime.minute == 0:
                            event += " {:%H}h".format(starttime)
                        else:
                            event += " {:%H:%M}".format(starttime)
                    if url:
                        event += " ({})".format(url)
                    yield event


def icalendar(name, url):
    def fetch():
        try:
            response = urllib.request.urlopen(url, timeout=1)
            return response.read().decode('utf-8')
        except urllib.error.URLError as e:
            print("icalendar:{}: {}".format(name, e))
            return None
    data = cache.get("{}.ics".format(name), 60 * 12, fetch)
    if data is None:
        # Cache empty and update failed.
        return
    icalendar_data(name, data)

def caldav(name, url):
    def build():
        cal = Calendar()
        dav = DAVClient(url)
        for calendar in dav.principal().calendars():
            for event in calendar.events():
                evcal = Calendar.from_ical(event.data)
                for e in evcal.walk():
                    if isinstance(e, Event):
                        cal.add_component(e)
        return cal.to_ical().decode('utf-8')
    data = cache.get("{}.ics".format(name), 60 * 12, build)
    if data is None:
        # Cache empty and update failed.
        return
    icalendar_data(name, data)
