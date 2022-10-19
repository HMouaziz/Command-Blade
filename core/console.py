from printy import printy
from . import commands
from .functions import get_terminal_width


def executor(command_name, arguments, command_dict):
    if arguments[0][0] != '-' or arguments[0] not in command_dict:
        printy(f' {arguments[0]} is not a recognized argument, you can find a list of valid arguments by using the'
               f' "-h" '
               f'argument.'.center(get_terminal_width()), '<r')
    elif arguments[0] == '-h':
        printy(command_dict['help_message'], 'n')
    else:
        class_name = getattr(commands, command_name)
        class_instance = class_name()
        class_instance.execute_command = getattr(class_instance, command_dict[arguments[0]])
        class_instance.execute_command()


def exit_command(args):
    command_name = 'Exit'
    command_dict = {'-h': 'help', '-': 'main_menu', '-f': 'exit',
                    'help_message': f'\n    Description:   Exits the console and returns to the main menu.\n\n    '
                                    f'Arguments:\n{"":8}-f{"":10}Exit CommandBlade fully as opposed to exiting the '
                                    f'console & returning to the main menu.\n{"":8}-h{"":10}Displays this message.'}
    executor(command_name=command_name, arguments=args, command_dict=command_dict)
