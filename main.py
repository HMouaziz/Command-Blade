from core.core import CommandBlade
from core.functions import Load


if __name__ == '__main__':
    debugger_mode = False
    if debugger_mode is True:
        pass
    else:
        plugins = Load.get_plugins()
        app = CommandBlade(plugins)
        app.run()

