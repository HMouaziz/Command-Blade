import importlib
import sys
from InquirerPy import inquirer
from printy import printy
from .utils import get_custom_style
from ..console.console import organise_console_input, call_command


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
