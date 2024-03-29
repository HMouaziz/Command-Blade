import random
import string
from InquirerPy import inquirer
from InquirerPy.base import Choice
from InquirerPy.validator import EmptyInputValidator
from core.interface import Interface
from core.functions import Settings


class Plugin:
    @staticmethod
    def process():
        print('Password Generator Plugin Loaded Successfully')

    @staticmethod
    def get_hook():
        ui_hook = {'ID': '02', 'module': 'password_generator', 'class': 'PasswordGenerator',
                   'method': 'password_generator_ui', 'choice_name': 'Password Generator'}
        return ui_hook


class PasswordGenerator:
    style = Interface.get_custom_style()

    @classmethod
    def password_generator_ui(cls):
        message = ""
        select = inquirer.select(
            message=message,
            choices=[
                Choice(value=1, name="Generate Password"),
                Choice(value=2, name="Settings"),
                Choice(value=None, name="Exit"),
            ],
            default=None,
            style=cls.style,
            qmark="≻≻",
            amark="≻≻"
        ).execute()
        if select == 1:
            settings = Settings.get()
            Interface.print(generate_password(settings['length'],
                                              settings['use_capitals'],
                                              settings['use_digits'],
                                              settings['use_symbols']
                                              ), 'y')
            cls.password_generator_ui()
        elif select == 2:
            cls.password_generator_settings_ui()
        elif select is None:
            choices, instruction_data = Interface.get_menu_list()
            Interface.main_menu(choices, instruction_data)

    @classmethod
    def password_generator_settings_ui(cls):
        message = ""
        settings = Settings.get()
        select = inquirer.select(
            message=message,
            choices=[
                Choice(value=1, name="Change password length"),
                Choice(value=2, name="Select character list"),
                Choice(value=None, name="Exit"),
            ],
            default=None,
            style=cls.style,
            qmark="≻≻",
            amark="≻≻"
        ).execute()
        if select == 1:
            settings['length'] = inquirer.number(
                message="Enter desired password length:",
                validate=EmptyInputValidator(),
            ).execute()
            Settings.update(settings)
        elif select == 2:
            selection = inquirer.checkbox(
                message="Select:",
                choices=[
                    Choice(value=1, name="Use capital letters (A-Z)"),
                    Choice(value=2, name="Use digits (0-9)"),
                    Choice(value=3, name="Use symbols (@!$%&*)")
                ],
                style=cls.style,
                qmark="≻≻",
                amark="≻≻"
            ).execute()
            if 1 in selection:
                settings["use_capitals"] = True
            elif 1 not in selection:
                settings["use_capitals"] = False
            if 2 in selection:
                settings["use_digits"] = True
            elif 2 not in selection:
                settings["use_digits"] = False
            if 3 in selection:
                settings["use_symbols"] = True
            elif 3 not in selection:
                settings["use_symbols"] = False
            Settings.update(settings)
        elif select is None:
            cls.password_generator_ui()
        cls.password_generator_settings_ui()


def generate_password(length, capital, digits, symbols):
    characters = ''
    if capital is True:
        characters = characters.join(string.ascii_letters)
    elif digits is True:
        characters = characters.join(string.digits)
    elif symbols is True:
        characters = characters.join(string.punctuation)
    elif capital is False:
        characters = characters.join(string.ascii_lowercase)
    password = ''.join(random.choice(characters) for _ in range(int(length)))
    return password
