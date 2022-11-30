"""This file contains all the functions that are related to the UI aspect of the core program"""

import importlib
import os
import sys
import tkinter
from tkinter import filedialog
from tkinter.messagebox import askokcancel
from InquirerPy import inquirer, get_style
from InquirerPy.base import Choice
from printy import printy
from pyfiglet import Figlet
from core.console.console import console_ui
from core.functions import Utils, Load


class Interface:
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

    @classmethod
    def main_menu(cls, choices, instruction_data):
        message = "Select Mode:"
        mode = inquirer.select(
            message=message,
            choices=choices,
            default=None,
            style=cls.style,
            qmark="≻≻",
            amark="≻≻"
        ).execute()
        if mode == 'console':
            console_ui(start_mode=True)
        elif mode == 'settings':
            cls.settings_ui()
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

    @classmethod
    def settings_ui(cls):
        pass

    @classmethod
    def get_input(cls, datatype, message, secret):
        if secret is True:
            data = inquirer.secret(message=message, transformer=lambda _: "[hidden]", style=cls.style, qmark="≻≻",
                                   amark="≻≻").execute()
        else:
            data = inquirer.text(message=message, style=cls.style, qmark="≻≻", amark="≻≻").execute()
        if datatype is str:
            if isinstance(data, str):
                return data
            else:
                input_string = str(data)
                return input_string
        else:
            return data

    @classmethod
    def get_custom_style(cls):
        return cls.style

    @classmethod
    def get_filepath(cls, mode='TK'):
        filepath = str
        if mode == 'TK':
            tkinter.Tk().withdraw()
            filepath = filedialog.askopenfilename()

        elif mode == 'IP':
            filepath = inquirer.text(message="Enter filepath:", style=cls.style, qmark="≻≻", amark="≻≻").execute()
        return filepath

    @classmethod
    def clear_screen(cls):
        clear = lambda: os.system('cls')
        clear()

    @classmethod
    def save_error_prompt(cls):
        answer = askokcancel(title='Error', message='The filepath you selected was not recognised.')
        return answer

    @classmethod
    def display_start_message(cls, message):
        width = Utils.get_terminal_width()
        m = Figlet(font='slant', width=width)
        printy(m.renderText("CommandBlade"), 'o')
        print(message.center(width))

    @classmethod
    def create_menu_list(cls, hooks):
        instruction_data = {}
        choices = [Choice(value='console', name="Console Mode", enabled=True), ]
        end = [Choice(value='settings', name="Settings", enabled=True), Choice(value=None, name="Exit", enabled=True)]
        for hook in hooks:
            choices.append(Choice(value=hook['UFI'], name=hook['choice_name'], enabled=True))
            instruction_data[hook['UFI']] = hook
        choices.extend(end)
        return choices, instruction_data

    @classmethod
    def get_menu_list(cls):
        hooks = Load.get_hooks()
        choices, instruction_data = cls.create_menu_list(hooks)
        return choices, instruction_data

    @classmethod
    def progress_bar(cls, iterable, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iterable    - Required  : iterable object (Iterable)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        total = len(iterable)

        # Progress Bar Printing Function
        def print_progress_bar(iteration):
            percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
            filled_length = int(length * iteration // total)
            bar = fill * filled_length + '-' * (length - filled_length)
            print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)

        # Initial Call
        print_progress_bar(0)
        # Update Progress Bar
        for i, item in enumerate(iterable):
            yield item
            print_progress_bar(i + 1)
        # Print New Line on Complete
        print()

