import pytz
from printy import printy
from core.functions import get_terminal_width, get_datetime_list, get_aware_datetime, print_all_recognised_tz


def exit_command(args=None):
    if args is None:
        from core.interface import main_menu
        main_menu()
    elif args[0] == '-f':
        exit(1)
    elif args[0] == '-h':
        printy(f'\n    Description:   Exits the console and returns to the main menu.\n\n    Arguments:\n'
               f'{"":8}-f{"":10}Exit CommandBlade fully as opposed to exiting the console & returning to the main menu.'
               f'\n{"":8}-h{"":10}Displays this message.', 'n')
    else:
        printy(f' {args[0]} is not a recognized argument, you can find a list of valid arguments below.'.center(
               get_terminal_width()) +
               f'\n    Arguments:\n'
               f'{"":8}-f{"":10}Exit CommandBlade fully as opposed to exiting the console & returning to the main menu.'
               f'\n{"":8}-h{"":10}Displays the help message.', '<r')


def help_command(args=None):
    if args is None:
        printy('help message', 'n')
    else:
        printy('Help does not accept arguments'.center(get_terminal_width()), '<r')


def time_command(args=None):
    datetime_list = get_datetime_list()
    if args is None:
        printy(f'The current local time is {datetime_list[1]}', 'y')
    elif args[0] == '-d':
        printy(f'It is {datetime_list[1].strftime("%I:%M %p on %A the %d of %B %G")}.', 'y')
    elif args[0] == '-tz':
        aware_datetime = get_aware_datetime(args[1])
        if len(args) == 1:
            printy('Timezone must be specified.'.center(get_terminal_width()), '<r')
            print_all_recognised_tz()
        if len(args) == 2:
            if args[1] in pytz.all_timezones:
                printy(f'It is {aware_datetime.strftime("%I:%M:%S %Z on %A the %d of %B %G")}', 'y')
            else:
                printy('Timezone not recognized'.center(get_terminal_width()), '<r')
                printy('Timezone is case sensitive!'.center(get_terminal_width()), '<r')
                print_all_recognised_tz()
    elif args[0] == '-u':
        printy(f'Unix timestamp as of {datetime_list[3].strftime("%c")} is {datetime_list[2]}', 'y')
    elif args[0] == '-h':
        printy(f'\n    Description:    Displays current local time.\n\n    Arguments:\n'
               f'{"":8}-d{"":10}Displays current local date and time.\n'
               f'{"":8}-tz{"":9}Displays current date and time at the specified timezone.\n'
               f'{"":8}-u{"":10}Displays unix time.\n'
               f'{"":8}-h{"":10}Displays this message.', 'n')
    else:
        printy(f'{args[0]} is not a recognized argument, you can find a list of valid arguments below.'.center(
               get_terminal_width()) +
               f'\n    Arguments:\n'
               f'{"":8}-d{"":10}Displays current local date and time.\n'
               f'{"":8}-tz{"":9}Displays current date and time at the specified timezone.\n'
               f'{"":8}-u{"":10}Displays unix timestamp.\n'
               f'{"":8}-h{"":10}Displays the help message.', '<r')
