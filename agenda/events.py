from agenda.helpers import *
from agenda.templates import *
from datetime import datetime
from typing import List, Iterable, Tuple

HIDDEN_TAGS = []

ENVIRONMENT = globals()

import os
import re
from xdg.BaseDirectory import save_config_path

from agenda.register import day_events, clear
__all__ = ['events_path', 'load_events', 'day_events', 'tag_filter', 'between', 'replace_tag']

def events_path() -> str:
    """Path where user event definitions are loaded from.

    They can be .py or .txt files.
    """
    return save_config_path('agenda')

def tag_filter(events, tags):
    """Filter event iterator by given tags."""
    for h in HIDDEN_TAGS:
        if h not in tags:
            tags.append('-' + h)
    included_res = [re.compile(r'{}\b'.format(re.escape(t))) for t in tags if not t.startswith('-')]
    excluded_res = [re.compile(r'{}\b'.format(re.escape(t[1:]))) for t in tags if t.startswith('-')]
    for e in events:
        if all(r.search(e) for r in included_res) and not any(r.search(e) for r in excluded_res):
            yield e

def replace_tag(item, tag, repl):
    assert tag.startswith('@')
    if repl == '':
        # If removing tag, remove preceeding spaces too.
        tag_re = r'\s*{}\b'.format(re.escape(tag))
    else:
        tag_re = r'{}\b'.format(re.escape(tag))
    return re.sub(tag_re, repl, item)




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
    """Load event definitions."""
    events_directories = [
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'events'),
        events_path(),
    ]
    clear()
    for events_dir in events_directories:
        for root, subdirs, files in os.walk(events_dir):
            for f in files:
                filename = os.path.join(root, f)
                if filename.endswith('.txt'):
                    load_txt(filename)
                elif filename.endswith('.py'):
                    load_py(filename)


def date_span(start: datetime, end: datetime, delta: timedelta=timedelta(days=1)):
    """Generate dates from 'start' to 'end', non-inclusive."""
    cur = start
    while cur < end:
        yield cur
        cur += delta

def on(day: datetime, tags: List[str]=[]) -> Iterable[Tuple[datetime, str]]:
    """Generate events for 'day', optionally filtered by tags."""
    return tag_filter(day_events(day), tags)

def between(start: datetime, end: datetime, tags: List[str]=[]) -> Iterable[Tuple[datetime, str]]:
    """Generate events from 'start' to 'end' (non-inclusive)
    """
    for day in date_span(start, end):
        for item in tag_filter(day_events(day), tags):
            yield day, item
