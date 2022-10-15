from InquirerPy import inquirer
from InquirerPy.base.control import Choice
import sys


def main_menu():
    message = "Command Blade"
    action = inquirer.select(
        message=message,
        choices=[
            "Command Runner",
            "WIP",
            Choice(value=None, name="Exit"),
        ],
        default=None,
    ).execute()
    if action == "Command Runner":
        pass
    elif action is None:
        print("Exiting...")
        sys.exit(1)

