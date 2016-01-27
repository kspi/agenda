from agenda.helpers import *
from agenda.templates import *
from datetime import datetime

ENVIRONMENT = globals()

import os
from xdg.BaseDirectory import save_config_path

def events_path():
    return save_config_path('agenda')


def load_py(filename):
    with open(filename) as f:
        code = compile(f.read(), filename, 'exec')
        exec(code, ENVIRONMENT)

def load_txt(filename):
    with open(filename) as f:
        for line in f:
            date_str, description = line.strip().split(' ', 1)
            date = datetime.strptime(date_str, "%Y-%m-%d")
            once(date.year, date.month, date.day, description)



def load_events():
    events_directories = [
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'events'),
        events_path(),
    ]
    for events_dir in events_directories:
        for root, subdirs, files in os.walk(events_dir):
            for f in files:
                filename = os.path.join(root, f)
                if filename.endswith('.txt'):
                    load_txt(filename)
                elif filename.endswith('.py'):
                    load_py(filename)

