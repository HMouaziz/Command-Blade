from InquirerPy import inquirer
from printy import printy


def exit_command(args=None):
    print(args)
    if args is None:
        from interface import main_menu
        main_menu()
    if args == '-f':
        print(args)
        confirm = inquirer.confirm(message="Are you sure you want to exit the program?", default=False).execute()
        if confirm is True:
            exit(1)
        else:
            pass
    elif args == '-h':
        printy(f'\n    Usage:   Exits the console and returns to the main menu.\n\n    Arguments:\n'
               f'{"":8}-f{"":10} Exit CommandBlade fully as opposed to exiting the console & returning to the main menu.'
               f'{"":8}-h{"":10} Shows this message.', 'n>')
