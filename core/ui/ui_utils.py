import inspect

from InquirerPy import get_style
from core import commands


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


def get_command_list():
    c_list = inspect.getmembers(commands, inspect.isclass)
    command_list = []
    for i in c_list:
        command_list.append(i[0])
    return command_list
