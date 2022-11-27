"""This file contains all main functions that are related to the UI aspect of the program"""

import importlib
import os
import sys
import tkinter
from tkinter import filedialog
from tkinter.messagebox import askokcancel
from InquirerPy import inquirer, get_style
from printy import printy
from pyfiglet import Figlet
from tkcolorpicker import askcolor
from core.console.console import organise_console_input, call_command
from core.functions import convert_hex, get_terminal_width


def main_menu(choices, instruction_data):
    style = get_custom_style()
    message = "Select Mode:"
    mode = inquirer.select(
        message=message,
        choices=choices,
        default=None,
        style=style,
        qmark="≻≻",
        amark="≻≻"
    ).execute()
    if mode == 'console':
        console_ui(start_mode=True)
    elif mode == 'settings':
        settings_ui()
    elif mode is None:
        print("Exiting...")
        sys.exit(1)
    else:
        for i in instruction_data:
            if mode == i:
                module_name = ''.join(('.', instruction_data[i]['module']))
                module = importlib.import_module(module_name, "plugins")
                class_name = getattr(module, instruction_data[i]['class'])
                class_instance = class_name()
                class_instance.run = getattr(class_instance, instruction_data[i]['method'])
                class_instance.run()


def console_ui(start_mode=False):
    if start_mode is True:
        printy("CommandBlade Console Version 0.3.6"
               "\nHalim Mouaziz, Project Hephaestus.", 'o>')
    style = get_custom_style()
    console_input = inquirer.text(message="", style=style, qmark="≻≻", amark="≻≻").execute()
    call_command(input_dict=organise_console_input(console_input))
    console_ui()


def settings_ui():
    pass


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


def display_start_message(message):
    width = get_terminal_width()
    m = Figlet(font='slant', width=width)
    printy(m.renderText("CommandBlade"), 'o')
    print(message.center(width))
