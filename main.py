from core.core import CommandBlade
from core.functions import Load
from plugins.mediocre_crypt import MediocreCrypt

if __name__ == '__main__':
    debugger_mode = False
    if debugger_mode is True:
        MediocreCrypt.decrypt_file()
    else:
        plugins = Load.get_plugins()
        app = CommandBlade(plugins)
        app.run()

