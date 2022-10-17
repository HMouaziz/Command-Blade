import sys
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from pyfiglet import Figlet
from printy import printy

import operations
from functions import get_terminal_width, get_custom_style, get_command_dict


def start():
    width = get_terminal_width()
    m = Figlet(font='slant', width=width)
    printy(m.renderText("CommandBlade"), 'o')
    print("[  CommandBlade v0.0.1, Halim Mouaziz  ]".center(width))
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
            Choice(value=4, name="Settings"),
            Choice(value=None, name="Exit"),
        ],
        default=None,
        style=style
    ).execute()
    if mode == 1:
        console_ui(start_mode=True)
    elif mode == 2:
        search_engine_ui()
    elif mode == 3:
        network_tools_ui()
    elif mode == 4:
        settings_ui()
    elif mode is None:
        print("Exiting...")
        sys.exit(1)


def console_ui(start_mode=False):
    style = get_custom_style()
    command_dict = get_command_dict()
    if start_mode is True:
        print("CommandBlade Console [Version 0.0.2]"
              "\nHalim Mouaziz, Project Hephaestus.")
    command = inquirer.text(message="", style=style).execute()
    command_name = command.split(' ', 1)[0]
    if command_name in command_dict.keys():
        parser = command_dict[command_name]
        run_parser = getattr(operations, parser)
        if command_name != command:
            args = command.split(' ', 1)[-1].split(' ')
            run_parser(args)
        else:
            run_parser()
    else:
        print(f'{command_name} is not a recognized command. '
              f'\n You can use the "help" command if you need a list of available commands.')
    console_ui()


def search_engine_ui():
    pass


def network_tools_ui():
    pass


def settings_ui():
    pass
