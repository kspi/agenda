from register import register_event
from helpers import *
from templates import *
from datetime import datetime


ENVIRONMENT = globals()

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



import os

EVENTS_DIRECTORIES = [
    os.path.join(os.path.dirname(os.path.realpath(__file__)), 'events'),
]

for events_dir in EVENTS_DIRECTORIES:
    for root, subdirs, files in os.walk(events_dir):
        for f in files:
            filename = os.path.join(root, f)
            if filename.endswith('.txt'):
                load_txt(filename)
            elif filename.endswith('.py'):
                load_py(filename)

