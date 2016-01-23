import ephem

@register_event
def moon_phases(day):
    if ephem.next_full_moon(day).datetime().date() == day:
        yield "Pilnatis"
    elif ephem.next_new_moon(day).datetime().date() == day:
        yield "Jaunatis"

@register_event
def equinoxes(day):
    spring_equinox = ephem.next_equinox(str(day.year))
    autumn_equinox = ephem.next_equinox(spring_equinox)
    if day == spring_equinox.datetime().date():
        yield "Pavasario lygiadienis"
    elif day == autumn_equinox.datetime().date():
        yield "Rudens lygiadienis"

@register_event
def solstices(day):
    summer_solstice = ephem.next_solstice(str(day.year))
    winter_solstice = ephem.next_solstice(summer_solstice)
    if day == summer_solstice.datetime().date():
        yield "Vasaros saulėgrįža"
    elif day == winter_solstice.datetime().date():
        yield "Žiemos saulėgrįža"
