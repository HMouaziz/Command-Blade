import json
import os

from InquirerPy import get_style, inquirer
import tkinter
from tkinter import filedialog


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


def get_input(is_string, message):
    style = get_custom_style()
    data = inquirer.text(message=message, style=style, qmark="≻≻", amark="≻≻").execute()
    if is_string is True:
        if isinstance(data, str):
            return data
        else:
            input_string = str(data)
            return input_string
    else:
        return data


def get_filepath():
    tkinter.Tk().withdraw()
    filepath = filedialog.askopenfilename()
    return filepath


def get_settings():
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    return settings


def update_settings(settings):
    with open('settings.json', 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)


def clear_screen():
    clear = lambda: os.system('cls')
    clear()
