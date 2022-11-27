from core.ui.interface import main_menu
from core.utils import get_hooks, create_menu_list, display_start_message


class Plugin:
    choices = []
    instruction_data = []

    def __init__(self):
        hooks = get_hooks()
        self.choices, self.instruction_data = create_menu_list(hooks)

    def process(self):
        hooks = get_hooks()
        create_menu_list(hooks)
        display_start_message("[  CommandBlade v0.1.4, Halim Mouaziz  ]")
        main_menu(self.choices, self.instruction_data)
