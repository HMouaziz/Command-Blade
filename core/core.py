import importlib

from printy import printy
from pyfiglet import Figlet

from core.utils import get_terminal_width
from core.ui.interface import main_menu


class CommandBlade:
    def __init__(self, plugins: list = []):
        if plugins:
            self._plugins = [
                importlib.import_module(plugin, ".plugins").Plugin() for plugin in plugins
            ]
        else:
            self._plugins = [importlib.import_module('.default', ".core").Plugin()]

    def run(self):
        width = get_terminal_width()
        m = Figlet(font='slant', width=width)
        printy(m.renderText("CommandBlade"), 'o')
        print("[  CommandBlade v0.0.1, Halim Mouaziz  ]".center(width))
        for plugin in self._plugins:
            plugin.process()
        main_menu()
