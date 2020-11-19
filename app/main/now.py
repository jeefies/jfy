import time


def now():
    t = time.localtime()
    timedict = {
        'year': t.tm_year,
        'mon': t.tm_mon,
        'day': t.tm_mday,
        'hour': t.tm_hour,
        'min': t.tm_min,
        'sec': t.tm_sec,
        'yday': t.tm_yday,
    }
    weekdays = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }
    timedict['wday'] = weekdays[t.tm_wday]
    return timedict
