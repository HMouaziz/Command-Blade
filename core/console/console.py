from printy import printy
from core.console.utils import get_command_list
from core.utils import get_terminal_width


def debugger():
    call_command(organise_console_input('command -t -b data'))


def organise_console_input(console_input):
    input_dict = {'command': '', 'argument': '-', 'modifiers': [], 'data': []}
    console_input = console_input.split(' ')
    input_dict['command'] = console_input[0]
    if len(console_input) == 1:
        pass
    elif len(console_input) == 2:
        if console_input[1][0] == '-':
            input_dict['argument'] = console_input[1]
        else:
            input_dict['data'].append(console_input[1])
    elif len(console_input) >= 3:
        console_input.pop(0)
        t = 0
        for i in console_input:
            if i[0] == '-':
                if t == 0:
                    input_dict['argument'] = i
                else:
                    input_dict['modifiers'].append(i)
                t += 1
            elif console_input[0] == '~':
                console_input.pop(0)
                data = "".join(console_input)
                input_dict['data'].append(data)
                break
            else:
                input_dict['data'].append(i)
    return input_dict


def call_command(input_dict):
    from core.console import commands
    try:
        if input_dict['command'].capitalize() in get_command_list():
            class_name = getattr(commands, input_dict['command'].capitalize())
            class_instance = class_name()
            class_instance.run = getattr(class_instance, 'feed_executor')
            class_instance.run(input_dict)
        elif input_dict['command'] == '':
            pass
        else:
            raise printy(f'{input_dict["command"]} is not a recognized command.'
                         f''.center(get_terminal_width()) +
                         f'\n You can use the "help" command if you need a list of available commands.'
                         f''.center(get_terminal_width()), '<r')
    except TypeError:
        pass


def executor(command_name, input_dict):
    from core.console import commands
    class_name = getattr(commands, command_name)
    class_instance = class_name()

    if input_dict['argument'] not in class_instance.argument_dict['arguments'] \
            or any(_ not in class_instance.argument_dict['modifiers'] for _ in input_dict['modifiers']) \
            or len(input_dict['modifiers']) > \
            class_instance.argument_behavior_dict[input_dict['argument']]['modifier_amount'] \
            or len(input_dict['data']) > class_instance.argument_behavior_dict[input_dict['argument']]['data_amount']:
        printy(class_instance.messages['argument_error'].center(get_terminal_width()), '<r')
    elif '-h' == input_dict['argument']:
        printy(class_instance.messages['help_message'], 'n')
    elif class_instance.argument_behavior_dict[input_dict['argument']]['modifier_amount'] > 0 \
            or class_instance.argument_behavior_dict[input_dict['argument']]['data_amount'] > 0:
        class_instance.execute_command = getattr(class_instance,
                                                 class_instance.argument_dict['arguments'][input_dict['argument']])
        class_instance.execute_command(input_dict)
    else:
        class_instance.execute_command = getattr(class_instance,
                                                 class_instance.argument_dict['arguments'][input_dict['argument']])
        class_instance.execute_command()
