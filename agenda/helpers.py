from datetime import timedelta, date

monday, tuesday, wednesday, thursday, friday, saturday, sunday = range(7)
mon, tue, wed, thur, fri, sat, sun = range(7)

def is_nth_weekday(weekday, n, day):
    """Returns true if `day` is the `n`-th `weekday` of its month.

    >>> is_nth_weekday(tuesday, 0, date(2016, 2, 2))
    True
    >>> is_nth_weekday(tuesday, 0, date(2016, 2, 3))
    False
    >>> is_nth_weekday(tuesday, 0, date(2016, 2, 9))
    False
    >>> is_nth_weekday(tuesday, 1, date(2016, 2, 9))
    True

    >>> is_nth_weekday(tuesday, 0, date(2016, 3, 1))
    True

    >>> is_nth_weekday(friday, -1, date(2016, 2, 26))
    True
    >>> is_nth_weekday(friday, -2, date(2016, 2, 26))
    False
    >>> is_nth_weekday(friday, -2, date(2016, 2, 19))
    True
    """
    if day.weekday() != weekday:
        return False
    if n >= 0:
        return (day.month == (day - timedelta(days=n * 7)).month
                and day.month != (day - timedelta(days=(n + 1) * 7)).month)
    else:
        n *= -1
        return ((n == 0 or day.month == (day + timedelta(days=(n - 1) * 7)).month)
                and day.month != (day + timedelta(days=n * 7)).month)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
