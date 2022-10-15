from InquirerPy import inquirer
from InquirerPy.base.control import Choice
import operations
from functions import mk_list_from
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
        command_runner_ui()
    elif action is None:
        print("Exiting...")
        sys.exit(1)


def command_runner_ui():
    action = inquirer.select(
        message="Command Runner",
        choices=[
            Choice(value=1, name="Run any command."),
            Choice(value=None, name="Return"),
        ],
        default=None,
    ).execute()
    if action == 1:
        run_fuzzy_command_ui()

    elif action is None:
        main_menu()


def run_fuzzy_command_ui():
    command_list = mk_list_from("command_operation_name.csv")

    action = inquirer.fuzzy(
        message="Run:",
        choices=command_list,
        default="",
    ).execute()
    if action is not None:
        operation = getattr(operations, action)
        operation()
    command_runner_ui()

