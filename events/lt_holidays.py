import ephem

yearly(1, 1, "Valstybinė šventė: naujieji metai")
yearly(2, 16, "Valstybinė šventė: Lietuvos valstybės atkūrimo diena (vėliava)")
yearly(3, 11, "Valstybinė šventė: Lietuvos nepriklausomybės atkūrimo diena (vėliava)")

@register_event
def easter(day):
    if (day.weekday() in frozenset([sunday, monday])
            and date(day.year, 3, 22) <= day <= date(day.year, 4, 25)):
        spring_equinox = ephem.next_equinox(str(day.year))
        full_moon = ephem.next_full_moon(spring_equinox)
        easter_day = full_moon.datetime().date() + timedelta(days=1)
        while easter_day.weekday() != sunday:
            easter_day += timedelta(days=1)
        if day == easter_day or day == easter_day + timedelta(days=1):
            yield "Valstybinė šventė: Velykos"

yearly(5, 1, "Valstybinė šventė: darbo diena")

@register_event
def mothers_day(day):
    if day.month == 5 and is_nth_weekday(sunday, 0, day):
        yield "Valstybinė šventė: motinos diena"

@register_event
def fathers_day(day):
    if day.month == 6 and is_nth_weekday(sunday, 0, day):
        yield "Valstybinė šventė: tėvo diena"

yearly(6, 24, "Valstybinė šventė: Rasos/Joninės")
yearly(7, 6, "Valstybinė šventė: Mindaugo karūnavimas (vėliava)")
yearly(8, 1, "Valstybinė šventė: Žolinė")
yearly(11, 1, "Valstybinė šventė: Visų šventųjų diena")
yearly(12, 24, "Valstybinė šventė: Kūčios")
yearly(12, 25, "Valstybinė šventė: Kalėdos")
yearly(12, 26, "Valstybinė šventė: Kalėdos")
