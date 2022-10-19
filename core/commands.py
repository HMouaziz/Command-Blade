import sys

import pytz
from printy import printy
from core.console import executor
from core.utils import get_datetime_list, get_terminal_width, print_all_recognised_tz, get_aware_datetime


class Command:
    @classmethod
    def feed_executor(cls, args):
        command_name = 'Name'
        command_dict = {'-': 'main',
                        'help_message': 'Default',
                        'arg_error_message': 'Default'}
        executor(command_name=command_name, arguments=args, command_dict=command_dict)


class Exit(Command):
    @classmethod
    def feed_executor(cls, args):
        command_name = 'Exit'
        command_dict = {'-': 'main_menu', '-h': 'help', '-f': 'exit',
                        'help_message': f'\n    Description:   Exits the console and returns to the main menu.\n\n    '
                                        f'Arguments:\n'
                                        f'{"":8}-f{"":10}Exit CommandBlade fully as opposed to exiting the console & '
                                        f'returning to the main menu.\n'
                                        f'{"":8}-h{"":10}Displays this message.',
                        'arg_error_message': f'{args[0]} is not a recognized argument, you can find a list of valid '
                                             f'arguments by using the "-h" argument.'}
        executor(command_name=command_name, arguments=args, command_dict=command_dict)

    @classmethod
    def exit(cls, args):
        sys.exit()

    @classmethod
    def main_menu(cls, args):
        from core.ui.interface import main_menu
        main_menu()


class Help(Command):
    @classmethod
    def feed_executor(cls, args):
        command_name = 'Help'
        command_dict = {'-': 'help',
                        'help_message': 'Help does not accept arguments',
                        'arg_error_message': 'Help does not accept arguments'}
        executor(command_name=command_name, arguments=args, command_dict=command_dict)

    @classmethod
    def help(cls, args):
        printy('help message', 'n')


class Time(Command):
    datetime_list = get_datetime_list()

    @classmethod
    def feed_executor(cls, args):
        command_name = 'Time'
        command_dict = {'-': 'time', '-d': 'date', '-tz': 'timezone', '-ptz': 'print_tz', '-u': 'unix', '-h': 'help',
                        'help_message': f'\n    Description:    Displays current local time.\n\n    Arguments:\n'
                                        f'{"":8}-d{"":10}Displays current local date and time.\n'
                                        f'{"":8}-tz{"":9}Displays current date and time at the specified timezone.\n'
                                        f'{"":8}-u{"":10}Displays unix time.\n'
                                        f'{"":8}-h{"":10}Displays this message.',
                        'arg_error_message': f'{args[0]} is not a recognized argument, you can find a list of valid '
                                             f'arguments by using the "-h" argument.'}
        executor(command_name=command_name, arguments=args, command_dict=command_dict)

    @classmethod
    def time(cls, args):
        printy(f'The current local time is {cls.datetime_list[1]}', 'y')

    @classmethod
    def date(cls, args):
        printy(f'It is {cls.datetime_list[1].strftime("%I:%M %p on %A the %d of %B %G")}.', 'y')

    @classmethod
    def timezone(cls, args):
        if len(args) == 1:
            printy('Timezone must be specified.'.center(get_terminal_width()), '<r')
        if len(args) == 2:
            aware_datetime = get_aware_datetime(args[1])
            if args[1] in pytz.all_timezones:
                printy(f'It is {aware_datetime.strftime("%I:%M:%S %Z on %A the %d of %B %G")}', 'y')
            else:
                printy('Timezone not recognized'.center(get_terminal_width()), '<r')
                printy('Timezone is case sensitive!'.center(get_terminal_width()), '<r')
                print_all_recognised_tz()

    @classmethod
    def print_tz(cls, args):
        print_all_recognised_tz()

    @classmethod
    def unix(cls, args):
        printy(f'Unix timestamp as of {cls.datetime_list[3].strftime("%c")} is {cls.datetime_list[2]}', 'y')

