import sys


class Command:
    pass


class Exit(Command):

    @classmethod
    def exit(cls):
        sys.exit()

    @classmethod
    def main_menu(cls):
        from core.interface import main_menu
        main_menu()
