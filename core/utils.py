import os
import time
import pytz
from datetime import datetime
from printy import printy


def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80


def get_datetime_list():
    datetime_list = [datetime.date(datetime.now()), datetime.time(datetime.now().replace(microsecond=0)),
                     time.time(), datetime.now()]
    return datetime_list


def get_aware_datetime(timezone):
    aware_datetime = datetime.now(pytz.timezone(timezone))
    return aware_datetime


def print_all_recognised_tz():
    printy(f'\n{"":8}Recognized timezone can be found below.\n', 'n')
    for a, b, c, d in zip(pytz.common_timezones[::4], pytz.common_timezones[1::4],
                          pytz.common_timezones[2::4], pytz.common_timezones[3::4]):
        printy(f'{a}{" " * (35 - len(a))}{b}{" " * (35 - len(b))}{c}{" " * (35 - len(c))}{d}', 'n')
