import re

from printy import printy
from core.console.utils import get_command_list
from core.utils import get_terminal_width


def debugger():
    call_command(organise_console_input('makeqr "www.project-hephaestus.com"'))


def organise_console_input(console_input):
    exception_list = ['calculate']
    input_dict = {'command': console_input.split(" ", 1).pop(0), 'argument': '-', 'modifiers': [], 'data': []}
    data_list = re.findall('\"[^\"]*[^\"]\"', console_input)
    if len(console_input.split(' ')) > 1:
        console_input = console_input.split(" ", 1)[1]
        if input_dict['command'] in exception_list:  # Will need update as more commands are added to exception list.
            input_dict['data'].append(console_input)
        else:
            if data_list:
                for i in data_list:
                    updated_console_input = console_input.replace(i, '[*placeholder*]')
                    console_input = updated_console_input
            if len(console_input.split(' ')) == 0:
                pass
            elif len(console_input.split(' ')) > 0:
                x, y = 0, 0
                for i in console_input.split(' '):
                    if i[0] == '-':
                        if x == 0:
                            input_dict['argument'] = i
                        else:
                            input_dict['modifiers'].append(i)
                        x += 1
                    elif i == '[*placeholder*]':
                        input_dict['data'].append(data_list[y])
                        y += 1
                    else:
                        input_dict['data'].append(i)
    else:
        pass
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
