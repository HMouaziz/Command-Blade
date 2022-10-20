import sys
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from pyfiglet import Figlet
from printy import printy
from .utils import get_custom_style
from ..console.console import organise_console_input, call_command
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
        printy("CommandBlade Console [Version 0.2.5]"
               "\nHalim Mouaziz, Project Hephaestus.", 'o>')
    style = get_custom_style()
    console_input = inquirer.text(message="", style=style, qmark="≻≻", amark="≻≻").execute()
    call_command(organise_console_input(console_input))
    console_ui()


def search_engine_ui():
    pass


def network_tools_ui():
    pass


def settings_ui():
    pass
