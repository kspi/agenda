EVENT_GENERATORS = []

def register_event(event_generator):
    EVENT_GENERATORS.append(event_generator)

def day_events(day):
    for gen in EVENT_GENERATORS:
        for event in gen(day):
            yield event

