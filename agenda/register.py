from datetime import datetime
from typing import Iterable

EVENT_GENERATORS = []

def clear():
    global EVENT_GENERATORS
    EVENT_GENERATORS = []

def register_event(event_generator):
    global EVENT_GENERATORS
    EVENT_GENERATORS.append(event_generator)

def day_events(day: datetime) -> Iterable[str]:
    """Generator of events for a given day."""
    global EVENT_GENERATORS
    for gen in EVENT_GENERATORS:
        for event in gen(day):
            yield event

