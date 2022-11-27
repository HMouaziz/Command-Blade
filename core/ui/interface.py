import importlib
import sys
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import EmptyInputValidator
from printy import printy
from .utils import get_custom_style, get_input, get_filepath
from ..utils import get_settings, update_settings
from ..console.console import organise_console_input, call_command
from ..hash_checker.operations import hash_string, hash_file
from ..password_generator.operations import generate_password


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


def hash_checker_ui():
    style = get_custom_style()
    message = "What kind of data type would you like to check?"
    select = inquirer.select(
        message=message,
        choices=[
            Choice(value=1, name="String"),
            Choice(value=2, name="File"),
            Choice(value=3, name="Settings"),
            Choice(value=None, name="Exit"),
        ],
        default=None,
        style=style,
        qmark="≻≻",
        amark="≻≻"
    ).execute()
    if select == 1:
        hash_algorithm = hash_algorithm_selector_ui()
        string_input = get_input(is_string=True, message="Enter string.")
        print(hash_string(hash_algorithm, string_input))
        hash_checker_ui()
    elif select == 2:
        hash_algorithm = hash_algorithm_selector_ui()
        filepath = get_filepath()
        print(filepath)
        hashed_file = hash_file(hash_algorithm, filepath)
        print(hashed_file.hexdigest())
        hash_checker_ui()
    elif select == 3:
        hash_checker_settings_ui()
    elif select is None:
        main_menu('a')


def hash_checker_settings_ui():
    style = get_custom_style()
    message = ""
    select = inquirer.select(
        message=message,
        choices=[
            Choice(value=1, name="Change hash algorithm"),
            Choice(value=None, name="Exit"),
        ],
        default=None,
        style=style,
        qmark="≻≻",
        amark="≻≻"
    ).execute()
    if select == 1:
        hash_algorithm_selector_ui()
    elif select is None:
        hash_checker_ui()


def hash_algorithm_selector_ui():
    function = inquirer.fuzzy(
        message="Select which hash algorithm you would like to use.",
        choices=[Choice(value="md5", name="MD5"),
                 Choice(value="sha1", name="SHA1"),
                 Choice(value="sha224", name="SHA224"),
                 Choice(value="sha256", name="SHA256"),
                 Choice(value="sha384", name="SHA384"),
                 Choice(value="sha512", name="SHA512"),
                 Choice(value="blake2b", name="BLAKE2B"),
                 Choice(value="blake2s", name="BLAKE2S")
                 ],
        default="",
    ).execute()
    return function


def password_generator_ui():
    style = get_custom_style()
    message = ""
    select = inquirer.select(
        message=message,
        choices=[
            Choice(value=1, name="Generate Password"),
            Choice(value=2, name="Settings"),
            Choice(value=None, name="Exit"),
        ],
        default=None,
        style=style,
        qmark="≻≻",
        amark="≻≻"
    ).execute()
    if select == 1:
        settings = get_settings()
        printy(generate_password(settings['p_type'],
                                 settings['length'],
                                 settings['use_capitals'],
                                 settings['use_digits'],
                                 settings['use_symbols']
                                 ), 'y')
        password_generator_ui()
    elif select == 2:
        password_generator_settings_ui()
    elif select is None:
        main_menu('a')


def password_generator_settings_ui():
    style = get_custom_style()
    message = ""
    settings = get_settings()
    select = inquirer.select(
        message=message,
        choices=[
            Choice(value=1, name="Change password length"),
            Choice(value=2, name="Change password type"),
            Choice(value=3, name="Select character list"),
            Choice(value=None, name="Exit"),
        ],
        default=None,
        style=style,
        qmark="≻≻",
        amark="≻≻"
    ).execute()
    if select == 1:
        settings['length'] = inquirer.number(
            message="Enter desired password length:",
            validate=EmptyInputValidator(),
        ).execute()
        update_settings(settings)
    elif select == 2:
        settings['p_type'] = inquirer.select(
            message='Select type:',
            choices=[
                Choice(value='Char', name="Characters"),
                Choice(value='Word', name="Words")
            ],
            style=style,
            qmark="≻≻",
            amark="≻≻"
        ).execute()
        update_settings(settings)
    elif select == 3:
        selection = inquirer.checkbox(
            message="Select:",
            choices=[
                Choice(value=1, name="Use capital letters (A-Z)"),
                Choice(value=2, name="Use digits (0-9)"),
                Choice(value=3, name="Use symbols (@!$%&*)")
            ],
            style=style,
            qmark="≻≻",
            amark="≻≻"
        ).execute()
        if 1 in selection:
            settings["use_capitals"] = True
        elif 1 not in selection:
            settings["use_capitals"] = False
        elif 2 in selection:
            settings["use_digits"] = True
        elif 2 not in selection:
            settings["use_digits"] = False
        elif 3 in selection:
            settings["use_symbols"] = True
        elif 3 not in selection:
            settings["use_symbols"] = False
        update_settings(settings)
    elif select is None:
        password_generator_ui()
    password_generator_settings_ui()



def settings_ui():
    pass
