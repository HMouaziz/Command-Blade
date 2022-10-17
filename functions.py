import os
import time
import pytz
from InquirerPy import get_style
from datetime import datetime

from printy import printy


def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80


def get_custom_style():
    style = get_style({"questionmark": "#ea6500",
                       "answermark": "#e5c07b",
                       "answer": "#ffffff",
                       "input": "#ea6500",
                       "question": "",
                       "answered_question": "",
                       "instruction": "#abb2bf",
                       "long_instruction": "#abb2bf",
                       "pointer": "#ea6500",
                       "checkbox": "#f06800",
                       "separator": "",
                       "skipped": "#5c6370",
                       "validator": "",
                       "marker": "#f06800",
                       "fuzzy_prompt": "#c678dd",
                       "fuzzy_info": "#abb2bf",
                       "fuzzy_border": "#ea6500",
                       "fuzzy_match": "#c678dd",
                       "spinner_pattern": "#e5c07b",
                       "spinner_text": ""}, style_override=True)
    return style


def get_command_dict():
    command_dict = {"help": "help_command", "exit": "exit_command", "time": "time_command"}
    return command_dict


def get_datetime_list():
    datetime_list = [datetime.date(datetime.now()), datetime.time(datetime.now().replace(microsecond=0)),
                     time.time(), datetime.now()]
    return datetime_list


def get_aware_datetime(timezone):
    aware_datetime = datetime.now(pytz.timezone(timezone))
    return aware_datetime


def print_all_recognised_tz():
    printy(f'{"":8}Recognized timezone can be found below.\n', 'n')
    for a, b, c, d in zip(pytz.common_timezones[::4], pytz.common_timezones[1::4],
                          pytz.common_timezones[2::4], pytz.common_timezones[3::4]):
        printy(f'{a}{" " * (35 - len(a))}{b}{" " * (35 - len(b))}{c}{" " * (35 - len(c))}{d}', 'n')
