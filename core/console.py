from printy import printy
from . import commands
from .utils import get_terminal_width


def executor(command_name, arguments, command_dict):
    if arguments[0][0] != '-' or arguments[0] not in command_dict:
        printy(command_dict['arg_error_message'].center(get_terminal_width()), '<r')
    elif arguments[0] == '-h':
        printy(command_dict['help_message'], 'n')
    else:
        class_name = getattr(commands, command_name)
        class_instance = class_name()
        class_instance.execute_command = getattr(class_instance, command_dict[arguments[0]])
        class_instance.execute_command(arguments)
