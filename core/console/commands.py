"""This file contains the Command class and its subclasses """

import io
import os
import sys
import pyqrcode as pyqrcode
import pytz
from printy import printy
from core.console.console import executor, console_ui
from plugins.hash_generator import hash_string, hash_file
from core.functions import Utils
from core.interface import Interface
from core.console.utils import get_datetime_list, get_aware_datetime, print_all_recognised_tz


class Command:
    command_name = 'Command'

    def __init__(self):
        self.messages = {'help_message': 'Help Default',
                         'argument_error': 'Error: Unrecognized or incomplete command line.'}
        self.argument_dict = {'arguments': {'-': 'main', '-h': 'help', '-t': 'test'},
                              'modifiers': {'-r': 'red', '-g': 'green', '-b': 'blue'}}
        self.argument_behavior_dict = {'-': {'accepted_modifiers': [], 'modifier_amount': 0, 'data_amount': 0},
                                       '-h': {'accepted_modifiers': [], 'modifier_amount': 0, 'data_amount': 0},
                                       '-t': {'accepted_modifiers': [], 'modifier_amount': 1, 'data_amount': 100}
                                       }

    @classmethod
    def feed_executor(cls, input_dict):
        executor(command_name=cls.command_name, input_dict=input_dict)

    @classmethod
    def main(cls):
        print('This is the Command class.')

    @classmethod
    def test(cls, input_dict):
        if '-r' in input_dict['modifiers']:
            for i in input_dict['data']:
                printy(i, 'r')
        elif '-g' in input_dict['modifiers']:
            for i in input_dict['data']:
                printy(i, 'n')
        elif '-b' in input_dict['modifiers']:
            for i in input_dict['data']:
                printy(i, 'b')
        else:
            for i in input_dict['data']:
                print(i)


class Calculate(Command):
    command_name = 'Calculate'

    def __init__(self):
        super().__init__()
        self.messages = {'help_message': f'\n    Description:   Calculates the expression given in between "".\n\n    '
                                         f'Arguments:\n'
                                         f'{"":8}-h{"":10}Displays this message.',
                         'argument_error': 'Error: Unrecognized or incomplete command line.'}
        self.argument_dict = {'arguments': {'-': 'calc', '-h': 'help'},
                              'modifiers': {}}
        self.argument_behavior_dict = {'-': {'accepted_modifiers': [], 'modifier_amount': 0, 'data_amount': 1},
                                       '-h': {'accepted_modifiers': [], 'modifier_amount': 0, 'data_amount': 0}
                                       }

    @classmethod
    def calc(cls, input_dict):
        equation = input_dict['data'][0]
        printy(eval(equation), 'y')


class Cls(Command):
    command_name = 'Cls'

    def __init__(self):
        super().__init__()
        self.messages = {'help_message': f'\n    Description:   Clears the console screen.\n',
                         'argument_error': 'Error: Unrecognized or incomplete command line.'}
        self.argument_dict = {'arguments': {'-': 'clear', '-h': 'help'},
                              'modifiers': {}}
        self.argument_behavior_dict = {'-': {'accepted_modifiers': [], 'modifier_amount': 0, 'data_amount': 0},
                                       '-h': {'accepted_modifiers': [], 'modifier_amount': 0, 'data_amount': 0}
                                       }

    @classmethod
    def clear(cls):
        clear = lambda: os.system('cls')
        clear()
        console_ui()


class Exit(Command):
    command_name = 'Exit'

    def __init__(self):
        super().__init__()
        self.messages = {'help_message': f'\n    Description:   Exits the console and returns to the main menu.\n\n    '
                                         f'Arguments:\n{"":8}-f{"":10}Exit CommandBlade fully as opposed to exiting '
                                         f'the console & returning to the main menu.\n'
                                         f'{"":8}-h{"":10}Displays this message.',
                         'argument_error': 'Error: Unrecognized or incomplete command line.'}
        self.argument_dict = {'arguments': {'-': 'main_menu', '-h': 'help', '-f': 'exit'},
                              'modifiers': {}}
        self.argument_behavior_dict = {'-': {'accepted_modifiers': [], 'modifier_amount': 0, 'data_amount': 0},
                                       '-h': {'accepted_modifiers': [], 'modifier_amount': 0, 'data_amount': 0},
                                       '-f': {'accepted_modifiers': [], 'modifier_amount': 0, 'data_amount': 0}
                                       }

    @classmethod
    def exit(cls):
        sys.exit()

    @classmethod
    def main_menu(cls):
        from core.interface import Interface
        choices, instruction_data = Interface.get_menu_list()
        Interface.main_menu(choices, instruction_data)


class Hash(Command):
    command_name = 'Hash'

    def __init__(self):
        super().__init__()
        self.messages = {'help_message': f'\n    Description:   Creates a hash from the chosen input in the chosen'
                                         f' algorithm\n\n    '
                                         f'Arguments:\n{"":8}-md5{"":10}Uses the md5 hash algorithm.\n'
                                         f'{"":8}-sha1{"":10}Uses the sha1 hash algorithm.\n'
                                         f'{"":8}-sha224{"":10}Uses the sha224 hash algorithm.\n'
                                         f'{"":8}-sha256{"":10}Uses the sha256 hash algorithm.\n'
                                         f'{"":8}-sha384{"":10}Uses the sha384 hash algorithm.\n'
                                         f'{"":8}-sha512{"":10}Uses the sha512 hash algorithm.\n'
                                         f'{"":8}-blake2b{"":10}Uses the blake2b hash algorithm.\n'
                                         f'{"":8}-blake2s{"":10}Uses the blake2s hash algorithm.\n'
                                         f'{"":8}-h{"":10}Displays this message.',
                         'argument_error': 'Error: Unrecognized or incomplete command line.'}
        self.argument_dict = {'arguments': {'-': 'hash_cmd', '-h': 'help', '-md5': 'hash_cmd', '-sha1': 'hash_cmd',
                                            '-sha224': 'hash_cmd', '-sha256': 'hash_cmd', '-sha384': 'hash_cmd',
                                            '-sha512': 'hash_cmd', '-blake2b': 'hash_cmd',
                                            '-blake2s': 'hash_cmd'
                                            },
                              'modifiers': {'-s': 'string', '-f': 'file', '-ui': 'use_get_filepath'}}
        self.argument_behavior_dict = {'-': {'accepted_modifiers': [], 'modifier_amount': 0, 'data_amount': 100},
                                       '-h': {'accepted_modifiers': [], 'modifier_amount': 0, 'data_amount': 0},
                                       '-md5': {'accepted_modifiers': ['-s', '-f', '-ui'], 'modifier_amount': 2,
                                                'data_amount': 100},
                                       '-sha1': {'accepted_modifiers': ['-s', '-f', '-ui'], 'modifier_amount': 2,
                                                 'data_amount': 100},
                                       '-sha224': {'accepted_modifiers': ['-s', '-f', '-ui'], 'modifier_amount': 2,
                                                   'data_amount': 100},
                                       '-sha256': {'accepted_modifiers': ['-s', '-f', '-ui'], 'modifier_amount': 2,
                                                   'data_amount': 100},
                                       '-sha384': {'accepted_modifiers': ['-s', '-f', '-ui'], 'modifier_amount': 2,
                                                   'data_amount': 100},
                                       '-sha512': {'accepted_modifiers': ['-s', '-f', '-ui'], 'modifier_amount': 2,
                                                   'data_amount': 100},
                                       '-blake2b': {'accepted_modifiers': ['-s', '-f', '-ui'], 'modifier_amount': 2,
                                                    'data_amount': 100},
                                       '-blake2s': {'accepted_modifiers': ['-s', '-f', '-ui'], 'modifier_amount': 2,
                                                    'data_amount': 100},
                                       }

    @classmethod
    def hash_cmd(cls, input_dict):
        algorithm = input_dict['argument'].upper()
        algorithm = algorithm[1:]
        if algorithm == '':
            algorithm = "SHA512"
        else:
            pass
        if not input_dict['modifiers'] or input_dict['modifiers'][0] == '-s':
            for i in input_dict['data']:
                printy(hash_string(algorithm, i), 'y')
        elif input_dict['modifiers'][0] == '-f':
            for i in input_dict['data']:
                hashed_file = hash_file(algorithm, i.replace('"', ''))
                printy(hashed_file.hexdigest(), 'y')
        elif input_dict['modifiers'][0] == '-ui':
            path = Interface.get_filepath()
            hashed_file = hash_file(algorithm, path)
            printy(hashed_file.hexdigest(), 'y')
        else:
            printy(f'Error: Unrecognized or incomplete command line.'
                   f''.center(Utils.get_terminal_width()), '<r')


class Makeqr(Command):
    command_name = 'Makeqr'

    def __init__(self):
        super().__init__()
        self.messages = {'help_message': f'\n    Description:   Generates a QR code from a URL.\n\n    '
                                         f'Arguments:\n{"":8}-dir{"":10} Lets you choose where the QR code is saved to.'
                                         f'\n'
                                         f'{"":8}-h{"":10}Displays this message.',
                         'argument_error': 'Error: Unrecognized or incomplete command line.'}
        self.argument_dict = {'arguments': {'-': 'simple_qr', '-h': 'help'},
                              'modifiers': {}}
        self.argument_behavior_dict = {'-': {'accepted_modifiers': [], 'modifier_amount': 0, 'data_amount': 1},
                                       '-h': {'accepted_modifiers': [], 'modifier_amount': 0, 'data_amount': 0}
                                       }

    @classmethod
    def simple_qr(cls, input_dict):
        url = pyqrcode.create(input_dict['data'][0])
        with open('qrcode.png', 'wb') as fstream:
            url.png(fstream, scale=5)
        url.png('qrcode.png', scale=5)
        buffer = io.BytesIO()
        url.png(buffer)
        print(list(buffer.getvalue()))


class Help(Command):
    command_name = 'Help'

    def __init__(self):
        super().__init__()
        self.messages = {'help_message': 'Help does not accept arguments',
                         'argument_error': 'Error: Unrecognized or incomplete command line.'}
        self.argument_dict = {'arguments': {'-': 'help', '-h': 'help'},
                              'modifiers': {}}
        self.argument_behavior_dict = {'-': {'accepted_modifiers': [], 'modifier_amount': 0, 'data_amount': 0},
                                       '-h': {'accepted_modifiers': [], 'modifier_amount': 0, 'data_amount': 0}
                                       }

    @classmethod
    def help(cls, args):
        printy('help message', 'n')


class Ping(Command):
    command_name = 'Ping'

    def __init__(self):
        super().__init__()
        self.messages = {'help_message': f'\n    Description:   Sends an echo request to a network host.\n\n    '
                                         f'Arguments:\n'
                                         f'{"":8}-h{"":10}Displays this message.',
                         'argument_error': 'Error: Unrecognized or incomplete command line.'}
        self.argument_dict = {'arguments': {'-': 'ping', '-h': 'help'},
                              'modifiers': {}}
        self.argument_behavior_dict = {'-': {'accepted_modifiers': [], 'modifier_amount': 0, 'data_amount': 0},
                                       '-h': {'accepted_modifiers': [], 'modifier_amount': 0, 'data_amount': 0}
                                       }

    @classmethod
    def ping(cls, args):
        print('ping is not ready yet!')


class Time(Command):
    command_name = 'Time'
    datetime_list = get_datetime_list()

    def __init__(self):
        super().__init__()
        self.messages = {'help_message': f'\n    Description:    Displays current local time.\n\n    Arguments:\n'
                                         f'{"":8}-d{"":10}Displays current local date and time.\n'
                                         f'{"":8}-tz{"":9}Displays current date and time at the specified timezone.\n'
                                         f'{"":8}-u{"":10}Displays unix time.\n'
                                         f'{"":8}-h{"":10}Displays this message.',
                         'argument_error': 'Error: Unrecognized or incomplete command line.'}
        self.argument_dict = {'arguments': {'-': 'time', '-h': 'help', '-d': 'date', '-tz': 'timezone',
                                            '-ptz': 'print_tz', '-u': 'unix'},
                              'modifiers': {}}
        self.argument_behavior_dict = {'-': {'accepted_modifiers': [], 'modifier_amount': 0, 'data_amount': 0},
                                       '-h': {'accepted_modifiers': [], 'modifier_amount': 0, 'data_amount': 0},
                                       '-d': {'accepted_modifiers': [], 'modifier_amount': 0, 'data_amount': 0},
                                       '-tz': {'accepted_modifiers': [], 'modifier_amount': 0, 'data_amount': 1},
                                       '-ptz': {'accepted_modifiers': [], 'modifier_amount': 0, 'data_amount': 0},
                                       '-u': {'accepted_modifiers': [], 'modifier_amount': 0, 'data_amount': 0}
                                       }

    @classmethod
    def time(cls):
        printy(f'The current local time is {cls.datetime_list[1]}', 'y')

    @classmethod
    def date(cls):
        printy(f'It is {cls.datetime_list[1].strftime("%I:%M %p on %A the %d of %B %G")}.', 'y')

    @classmethod
    def timezone(cls, input_dict):
        if len(input_dict['data']) == 0:
            printy('Timezone must be specified.'.center(Utils.get_terminal_width()), '<r')
        elif input_dict['data'][0] in pytz.all_timezones:
            aware_datetime = get_aware_datetime(input_dict['data'][0])
            printy(f'It is {aware_datetime.strftime("%I:%M:%S %Z on %A the %d of %B %G")}', 'y')
        else:
            printy('Timezone not recognised'.center(Utils.get_terminal_width()), '<r')
            printy('Timezone is case sensitive!'.center(Utils.get_terminal_width()), '<r')
            printy('You can obtain a list of recognised timezones by using the "-ptz" argument'
                   .center(Utils.get_terminal_width()), '<r')

    @classmethod
    def print_tz(cls):
        print_all_recognised_tz()

    @classmethod
    def unix(cls):
        printy(f'Unix timestamp as of {cls.datetime_list[3].strftime("%c")} is {cls.datetime_list[2]}', 'y')
