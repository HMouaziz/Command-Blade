import sys
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from pyfiglet import Figlet
from printy import printy
from .utils import get_custom_style
from ..console.console import organise_console_input, call_command
from ..hash_checker.operations import hash_string
from ..utils import get_terminal_width


def start():
    width = get_terminal_width()
    m = Figlet(font='slant', width=width)
    printy(m.renderText("CommandBlade"), 'o')
    print("[  CommandBlade v0.0.2, Halim Mouaziz  ]".center(width))
    main_menu()


def main_menu():
    style = get_custom_style()
    message = "Select Mode:"
    mode = inquirer.select(
        message=message,
        choices=[
            Choice(value=1, name="Console Mode"),
            Choice(value=2, name="Search Engine Mode"),
            Choice(value=3, name="Network Tools Mode"),
            Choice(value=4, name="Hash Checker"),
            Choice(value=5, name="Settings"),
            Choice(value=None, name="Exit"),
        ],
        default=None,
        style=style,
        qmark="≻≻",
        amark="≻≻"
    ).execute()
    if mode == 1:
        console_ui(start_mode=True)
    elif mode == 2:
        search_engine_ui()
    elif mode == 3:
        network_tools_ui()
    elif mode == 4:
        hash_checker_ui()
    elif mode == 5:
        settings_ui()
    elif mode is None:
        print("Exiting...")
        sys.exit(1)


def console_ui(start_mode=False):
    if start_mode is True:
        printy("CommandBlade Console Version 0.2.5"
               "\nHalim Mouaziz, Project Hephaestus.", 'o>')
    style = get_custom_style()
    console_input = inquirer.text(message="", style=style, qmark="≻≻", amark="≻≻").execute()
    call_command(input_dict=organise_console_input(console_input))
    console_ui()


def search_engine_ui():
    pass


def network_tools_ui():
    pass


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
        pass
    elif select == 3:
        hash_checker_settings_ui()
    elif select is None:
        main_menu()


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
        choices=["MD5", "SHA1", "SHA224", "SHA256", "SHA384", "SHA512", "blake2b", "blake2s"],
        default="",
    ).execute()
    return function


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


def settings_ui():
    pass
