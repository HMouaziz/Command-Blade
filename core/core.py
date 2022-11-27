import importlib


class CommandBlade:
    def __init__(self, plugins: list = []):
        if plugins:
            self._plugins = [
                importlib.import_module(plugin, "plugins").Plugin() for plugin in plugins
            ]
        else:
            self._plugins = [importlib.import_module('.default', "plugins").Plugin()]

    def run(self):
        for plugin in self._plugins:
            plugin.process()
