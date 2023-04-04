"""Default plugin, initializes program."""
from core.interface import Interface
from core.functions import Load, APILoader


class Plugin:
    choices = []
    instruction_data = []

    def __init__(self):
        hooks = Load.get_hooks()
        self.choices, self.instruction_data = Interface.create_menu_list(hooks)

    def process(self):
        APILoader.load_env()
        Interface.display_start_message("[  CommandBlade v0.1.6, Halim Mouaziz  ]")
        Interface.main_menu(self.choices, self.instruction_data)
