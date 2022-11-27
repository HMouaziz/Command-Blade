"""This file contains standardised functions that can be used by plugins and the core program."""

import importlib
import json
import os
from os import listdir
from os.path import isfile, join


class Load:
    @classmethod
    def get_plugins(cls, start=False):
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

    @classmethod
    def get_hooks(cls):
        plugin_list = cls.get_plugins()
        plugin_list.remove('.default')
        hooks = []
        for i in plugin_list:
            plugin = importlib.import_module(i, "plugins")
            class_name = getattr(plugin, 'Plugin')
            class_instance = class_name()
            class_instance.run = getattr(class_instance, 'get_hook')
            hooks.append(class_instance.run())
        return hooks


class Settings:
    @classmethod
    def get(cls):
        with open('settings.json', 'r') as f:
            settings = json.load(f)
        return settings

    @classmethod
    def update(cls, settings):
        with open('settings.json', 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)


class FileUtil:
    @classmethod
    def get_filetype(cls, filepath):
        filename, filetype = os.path.splitext(filepath)
        split_path = (filename, filetype)
        return split_path


def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80
