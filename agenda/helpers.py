from datetime import timedelta, date

monday, tuesday, wednesday, thursday, friday, saturday, sunday = range(7)
mon, tue, wed, thur, fri, sat, sun = range(7)

def is_nth_weekday(weekday, n, day):
    if day.weekday() != weekday:
        return False
    if n >= 0:
        n += 1
        return ((n == 0 or day.month == (day - timedelta(days=(n - 1) * 7)).month)
                and day.month != (day - timedelta(days=n * 7)).month)
    else:
        n *= -1
        return ((n == 0 or day.month == (day + timedelta(days=(n - 1) * 7)).month)
                and day.month != (day + timedelta(days=n * 7)).month)
