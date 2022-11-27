"""This file contains standardised functions that can be used by plugins and the core program."""

import importlib
import json
import os
from os import listdir
from os.path import isfile, join
from InquirerPy.base import Choice


def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80


def get_plugins(start=False):
    plugin_list = []
    p_list = [f for f in listdir('plugins') if isfile(join('plugins', f))]
    for i in p_list:
        if not i.endswith('.py'):
            p_list.remove(i)
        else:
            i = i.split('.')[0]
            plugin_list.append(f'.{i}')
    plugin_list.append(plugin_list.pop(plugin_list.index('.default')))
    if len(plugin_list) < 2 and start is True:
        print("No Plugins Detected")
    return plugin_list


def get_hooks():
    plugin_list = get_plugins()
    plugin_list.remove('.default')
    hooks = []
    for i in plugin_list:
        plugin = importlib.import_module(i, "plugins")
        class_name = getattr(plugin, 'Plugin')
        class_instance = class_name()
        class_instance.run = getattr(class_instance, 'get_hook')
        hooks.append(class_instance.run())
    return hooks


def create_menu_list(hooks):
    instruction_data = {}
    choices = [Choice(value='console', name="Console Mode", enabled=True), ]
    end = [Choice(value='settings', name="Settings", enabled=True), Choice(value=None, name="Exit", enabled=True)]
    for hook in hooks:
        choices.append(Choice(value=hook['UFI'], name=hook['choice_name'], enabled=True))
        instruction_data[hook['UFI']] = hook
    choices.extend(end)
    return choices, instruction_data


def get_menu_list():
    hooks = get_hooks()
    choices, instruction_data = create_menu_list(hooks)
    return choices, instruction_data


def get_filetype(filepath):
    filename, filetype = os.path.splitext(filepath)
    split_path = (filename, filetype)
    return split_path


def get_settings():
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    return settings


def update_settings(settings):
    with open('settings.json', 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)


def convert_hex(hex_color):
    hexi = hex_color[1:]
    rgb_color = tuple(int(hexi[i:i+2], 16) for i in (0, 2, 4))
    rgba_color = list([int(hexi[x:x+2], 16)for x in (0, 2, 4)])
    rgba_color.append(int("{:0.0f}".format([int(hexi[6:], 16)/255][0] * 255)))
    return rgb_color, rgba_color
