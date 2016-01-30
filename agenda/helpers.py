from datetime import timedelta, date

monday, tuesday, wednesday, thursday, friday, saturday, sunday = range(7)
mon, tue, wed, thur, fri, sat, sun = range(7)

def is_nth_weekday(weekday, n, day):
    d = n + 1 if n >= 0 else n
    return day.weekday() == weekday and day.month != (day - timedelta(days=d * 7)).month
