import inspect
import sys
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from pyfiglet import Figlet
from printy import printy
from core import commands
from .ui_utils import get_custom_style, get_command_list
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
            Choice(value=4, name="Settings"),
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
        settings_ui()
    elif mode is None:
        print("Exiting...")
        sys.exit(1)


def console_ui(start_mode=False):
    if start_mode is True:
        printy("CommandBlade Console [Version 0.1.3]"
               "\nHalim Mouaziz, Project Hephaestus.", 'o>')
    style = get_custom_style()
    command = inquirer.text(message="", style=style, qmark="≻≻", amark="≻≻").execute()
    command_name = command.split(' ', 1)[0]
    try:
        if command_name.capitalize() in get_command_list():
            class_name = getattr(commands, command_name.capitalize())
            class_instance = class_name()
            class_instance.run = getattr(class_instance, 'feed_executor')
            if command_name != command:
                args = command.split(' ', 1)[-1].split(' ')
                class_instance.run(args)
            else:
                class_instance.run(args='-')
        else:
            raise printy(f'{command_name} is not a recognized command. '.center(get_terminal_width()) +
                         f'\n You can use the "help" command if you need a list of available commands.'
                         f''.center(get_terminal_width()), '<r')
    except TypeError:
        pass
    console_ui()


def search_engine_ui():
    pass


def network_tools_ui():
    pass


def settings_ui():
    pass
