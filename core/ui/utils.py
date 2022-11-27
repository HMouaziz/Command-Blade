import os
from tkinter.messagebox import askokcancel

from InquirerPy import get_style, inquirer
import tkinter
from tkinter import filedialog

from tkcolorpicker import askcolor

from core.utils import convert_hex


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


def clear_screen():
    clear = lambda: os.system('cls')
    clear()


def get_color_picker(color_dict):
    old_color = color_dict['SVG']
    hex_color = askcolor(old_color, alpha=True)[-1]
    rgb_color, rgba_color = convert_hex(hex_color)
    new_color = {'PNG': rgba_color, 'SVG': hex_color, 'EPS': rgb_color}
    return new_color


def save_error_prompt():
    answer = askokcancel(title='Error', message='The filepath you selected was not recognised.')
    return answer
