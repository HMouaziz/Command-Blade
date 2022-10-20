from printy import printy
from core.console.utils import get_command_list

from core.utils import get_terminal_width


def organise_console_input(console_input):
    input_dict = {'command': '', 'arguments': ['-'], 'data': []}
    console_input = console_input.split(' ')
    input_dict['command'] = console_input[0]
    if len(console_input) == 1:
        pass
    elif len(console_input) == 2:
        if console_input[1][0] == '-':
            input_dict['arguments'][0] = console_input[1]
        else:
            input_dict['data'].append(console_input[1])
    elif len(console_input) >= 3:
        console_input.pop(0)
        t = 0
        for i in console_input:
            if i[0] == '-':
                if t == 0:
                    input_dict['arguments'][0] = i
                else:
                    input_dict['arguments'].append(i)
                t += 1
            else:
                input_dict['data'].append(i)
    organised_input_dict = input_dict
    return organised_input_dict


def call_command(organised_input_dict):
    from core.console import commands
    try:
        if organised_input_dict['command'].capitalize() in get_command_list():
            class_name = getattr(commands, organised_input_dict['command'].capitalize())
            class_instance = class_name()
            class_instance.run = getattr(class_instance, 'feed_executor')
            class_instance.run(organised_input_dict['arguments'][0])
        elif organised_input_dict['command'] == '':
            pass
        else:
            raise printy(f'{organised_input_dict["command"]} is not a recognized command.'
                         f''.center(get_terminal_width()) +
                         f'\n You can use the "help" command if you need a list of available commands.'
                         f''.center(get_terminal_width()), '<r')
    except TypeError:
        pass


def executor(command_name, arguments, command_dict):
    from core.console import commands
    if arguments[0][0] != '-' or arguments[0] not in command_dict:
        printy(command_dict['arg_error_message'].center(get_terminal_width()), '<r')
    elif arguments[0] == '-h':
        printy(command_dict['help_message'], 'n')
    else:
        class_name = getattr(commands, command_name)
        class_instance = class_name()
        class_instance.execute_command = getattr(class_instance, command_dict[arguments[0]])
        class_instance.execute_command(arguments)
