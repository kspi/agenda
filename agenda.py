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
import http.server

DAYS = 62

def datespan(start, end, delta=timedelta(days=1)):
    cur = start
    while cur < end:
        yield cur
        cur += delta

def get_ical():
    today = date.today()
    prevday = today
    calendar = icalendar.Calendar()
    for day in datespan(today, today + timedelta(days=DAYS)):
        events = list(day_events(day))
        for name in events:
            event = icalendar.Event()
            event.add('SUMMARY', name)
            event.add('DTSTART', day)
            event.add('DTEND', day)
            calendar.add_component(event)
    return calendar.to_ical()

def print_text():
    today = date.today()
    prevday = today
    for day in datespan(today, today + timedelta(days=16)):
        events = list(day_events(day))
        if events:
            print(day.strftime("%F %A"))
            for event in events:
                print(event)
            print()


class AgendaHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/calendar; charset=utf-8")
        self.end_headers()
        self.wfile.write(get_ical())

def server():
    httpd = http.server.HTTPServer(('localhost', 7000), AgendaHTTPRequestHandler)
    print("Serving on http://localhost:7000 ...")
    httpd.serve_forever()


def main():
    locale.setlocale(locale.LC_TIME, "lt_LT.utf8")

    if len(sys.argv) > 1 and sys.argv[1] == '--ical':
        print(get_ical())
    elif len(sys.argv) > 1 and sys.argv[1] == '--server':
        server()
    else:
        print_text()


if __name__ == '__main__':
    main()
