from datetime import datetime
from typing import Iterable

EVENT_GENERATORS = []

def register_event(event_generator):
    EVENT_GENERATORS.append(event_generator)

def day_events(day: datetime) -> Iterable[str]:
    """Generator of events for a given day."""
    for gen in EVENT_GENERATORS:
        for event in gen(day):
            yield event

