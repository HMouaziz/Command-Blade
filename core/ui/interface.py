import importlib
import sys
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from printy import printy
from .utils import get_custom_style, get_input, get_filepath
from ..console.console import organise_console_input, call_command
from ..hash_checker.operations import hash_string, hash_file


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


def settings_ui():
    pass
