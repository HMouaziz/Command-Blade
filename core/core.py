"""This file contains the main Class for the program"""

import importlib


class CommandBlade:
    def __init__(self, plugins: list = []):
        """Loads the plugins"""
        if plugins:
            self._plugins = [
                importlib.import_module(plugin, "plugins").Plugin() for plugin in plugins
            ]
        else:
            self._plugins = [importlib.import_module('.default', "plugins").Plugin()]

    def run(self):
        """Runs the plugins"""
        for plugin in self._plugins:
            plugin.process()
