from core.core import CommandBlade
from core.functions import get_plugins
from core.console import console

if __name__ == '__main__':
    debugger_mode = False
    if debugger_mode is True:
        console.debugger()
    else:
        plugins = get_plugins()
        app = CommandBlade(plugins)
        app.run()

