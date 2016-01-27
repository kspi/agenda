import parsedatetime
from agenda.events import events_path
import os

def add(date, description):
    cal = parsedatetime.Calendar()
    date_parsed, _ = cal.parseDT(date)
    filename = os.path.join(events_path(), "{:%Y}.txt".format(date_parsed))
    line = "{:%F} {}".format(date_parsed, description)
    with open(filename, 'a') as f:
        print(line, file=f)
    print(line)
