"""This file contains all the functions that are related to the UI aspect of the core program,
   and UI related functions that can be used by both plugins and the core program."""

import importlib
import os
import sys
import tkinter
from tkinter import filedialog
from tkinter.messagebox import askokcancel
from InquirerPy import inquirer
from InquirerPy.base import Choice
from InquirerPy.validator import EmptyInputValidator, PathValidator
from printy import printy
from pyfiglet import Figlet
from core.console.console import console_ui
from core.exceptions import ValidationValueError
from core.functions import Utils, Load, Settings


class Interface:
    style = Settings.get_style()

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
    def print(cls, x, y=None):
        """See printy docs for info: https://github.com/edraobdu/printy#how-to-use-it"""
        printy(x, y)

    @classmethod
    def get_string(cls, message):
        data = inquirer.text(message=message, style=cls.style, qmark="≻≻", amark="≻≻").execute()
        return data

    @classmethod
    def get_num(cls, message, float_allowed=False, default=None, min_allowed=None, max_allowed=None, mandatory=True):
        data = inquirer.number(message=message, float_allowed=float_allowed, default=default, min_allowed=min_allowed,
                               max_allowed=max_allowed, mandatory=mandatory, style=cls.style, qmark="≻≻", amark="≻≻"
                               ).execute()
        if float_allowed is True:
            return float(data)
        else:
            return int(data)

    @classmethod
    def get_validated_num(cls, message, float_allowed=False, default=None, min_allowed=None, max_allowed=None,
                          mandatory=True):
        data = inquirer.number(message=message, float_allowed=float_allowed, default=default, min_allowed=min_allowed,
                               max_allowed=max_allowed, mandatory=mandatory, style=cls.style, qmark="≻≻", amark="≻≻",
                               validate=EmptyInputValidator()).execute()
        if float_allowed is True:
            return float(data)
        else:
            return int(data)

    @classmethod
    def get_secret(cls, message, secret):
        secret = inquirer.secret(message=message, validate=lambda text: text == secret, style=cls.style, qmark="≻≻",
                                 amark="≻≻").execute()
        return secret

    @classmethod
    def confirm(cls, message):
        result = inquirer.confirm(message=message, style=cls.style, qmark="≻≻", amark="≻≻").execute()
        return result

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
    def get_filepath(cls, message, validate, default=None):
        if default is None:
            default = "~/" if os.name == "posix" else "C:\\"
        if validate == "FILE":
            filepath = inquirer.filepath(message=message, default=default,
                                         validate=PathValidator(is_file=True, message="Input must be a file")).execute()
        elif validate == "DIRECTORY":
            filepath = inquirer.filepath(message=message, default=default,
                                         validate=PathValidator(is_file=True, message="Input must be a file")).execute()
        else:
            raise ValidationValueError(f"Validate must be set to 'FILE' or 'DIRECTORY' cannot be: {validate}.")
        return filepath

    @classmethod
    def get_filepath_gui(cls):
        tkinter.Tk().withdraw()
        filepath = filedialog.askopenfilename()
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
        end = [Choice(value=None, name="Exit", enabled=True)]
        for hook in hooks:
            choices.append(Choice(value=hook['ID'], name=hook['choice_name'], enabled=True))
            instruction_data[hook['ID']] = hook
        choices.extend(end)
        return choices, instruction_data

    @classmethod
    def get_menu_list(cls):
        hooks = Load.get_hooks()
        choices, instruction_data = cls.create_menu_list(hooks)
        return choices, instruction_data
