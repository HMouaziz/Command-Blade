# CommandBlade Documentation

## Overview

CommandBlade is a versatile command-line application framework designed to streamline the development and execution of custom plugins. It allows you to load, manage, and run various plugins effortlessly.

## Table of Contents

- [Installation](#installation)
- [Getting Started](#getting-started)
- [Core Classes and Functions](#core-classes-and-functions)
  - [CommandBlade](#commandblade)
  - [Load](#load)
  - [APILoader](#apiloader)
  - [Settings](#settings)
  - [FileUtil](#fileutil)
  - [Utils](#utils)
  - [Interface](#interface)
- [Creating Plugins](#creating-plugins)
- [Running the Application](#running-the-application)
- [Example Plugins](#example-plugins)

## Installation

To install CommandBlade, clone the repository and install the required dependencies:

```bash
git clone <repository_url>
cd CommandBlade
pip install -r requirements.txt
```

## Getting Started

To start using CommandBlade, follow these steps:

1. Ensure your plugins are placed in the `plugins` directory.
2. Run the application:

```bash
python main.py
```

## Core Classes and Functions

### CommandBlade

The `CommandBlade` class is responsible for loading and running the plugins.

```python
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
```

### Load

The `Load` class handles the loading of plugins and hooks.

```python
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
```

### APILoader

The `APILoader` class loads environment variables.

```python
class APILoader:
    @classmethod
    def load_env(cls):
        load_dotenv()
```

### Settings

The `Settings` class manages application settings.

```python
class Settings:
    @classmethod
    def get_style(cls):
        return get_style({
            "questionmark": "#ea6500",
            "answermark": "#e5c07b",
            "answer": "#ffffff",
            "input": "#ea6500",
            "question": "",
            "answered_question": "",
            "instruction": "#abb2bf",
            "long_instruction": "#abb2bf",
            "pointer": "#ea6500",
            "checkbox": "#f06800",
            "separator": "",
            "skipped": "#5c6370",
            "validator": "",
            "marker": "#f06800",
            "fuzzy_prompt": "#c678dd",
            "fuzzy_info": "#abb2bf",
            "fuzzy_border": "#ea6500",
            "fuzzy_match": "#c678dd",
            "spinner_pattern": "#e5c07b",
            "spinner_text": ""
        }, style_override=True)

    @classmethod
    def get(cls):
        with open('settings.json', 'r') as f:
            settings = json.load(f)
        return settings

    @classmethod
    def update(cls, settings):
        with open('settings.json', 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
```

### FileUtil

The `FileUtil` class provides utility functions for file handling.

```python
class FileUtil:
    @classmethod
    def get_filetype(cls, filepath):
        filename, file_type = os.path.splitext(filepath)
        return filename, file_type

    @classmethod
    def get_magic_filetype(cls, filepath):
        file_type = filetype.guess(filepath)
        if file_type is None:
            return None
        return file_type.extension
```

### Utils

The `Utils` class provides general utility functions.

```python
class Utils:
    @classmethod
    def get_ip(cls):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip

    @staticmethod
    def check_instance(name: str, instance, value):
        if not isinstance(value, instance):
            raise TypeError(f"{name} must be {instance}.")

    @staticmethod
    def chunked(size, source):
        for i in range(0, len(source), size):
            yield source[i:i + size]

    @classmethod
    def get_terminal_width(cls):
        try:
            return os.get_terminal_size().columns
        except OSError:
            return 80
```

### Interface

The `Interface` class manages the user interface and interactions.

```python
class Interface:
    style = Settings.get_style()

    @classmethod
    def main_menu(cls, choices, instruction_data):
        message = "Select Mode:"
        mode = inquirer.select(
            message=message,
            choices=choices,
            default=None,
            style=cls.style,
            qmark="≻≻",
            amark="≻≻"
        ).execute()
        if mode == 'console':
            console_ui(start_mode=True)
        elif mode is None:
            print("Exiting...")
            sys.exit(1)
        else:
            for i in instruction_data:
                if mode == i:
                    module_name = ''.join(('.', instruction_data[i]['module']))
                    module = importlib.import_module(module_name, "plugins")
                    class_name = getattr(module, instruction_data[i]['class'])
                    class_instance = class_name()
                    class_instance.run = getattr(class_instance, instruction_data[i]['method'])
                    class_instance.run()

    @classmethod
    def print(cls, x, y=None):
        printy(x, y)

    @classmethod
    def get_string(cls, message):
        data = inquirer.text(message=message, style=cls.style, qmark="≻≻", amark="≻≻").execute()
        return data

    @classmethod
    def get_num(cls, message, float_allowed=False, default=None, min_allowed=None, max_allowed=None, mandatory=True):
        data = inquirer.number(message=message, float_allowed=float_allowed, default=default, min_allowed=min_allowed,
                               max_allowed=max_allowed, mandatory=mandatory, style=cls.style, qmark="≻≻", amark="≻≻"
                               ).execute()
        if float_allowed:
            return float(data)
        return int(data)

    @classmethod
    def get_validated_num(cls, message, float_allowed=False, default=None, min_allowed=None, max_allowed=None,
                          mandatory=True):
        data = inquirer.number(message=message, float_allowed=float_allowed, default=default, min_allowed=min_allowed,
                               max_allowed=max_allowed, mandatory=mandatory, style=cls.style, qmark="≻≻", amark="≻≻",
                               validate=EmptyInputValidator()).execute()
        if float_allowed:
            return float(data)
        return int(data)

    @classmethod
    def get_secret(cls, message, secret):
        secret = inquirer.secret(message=message, validate=lambda text: text == secret, style=cls.style, qmark="≻≻",
                                 amark="≻≻").execute()
        return secret

    @classmethod
    def confirm(cls, message):
        result = inquirer.confirm(message=message, style=cls.style, qmark="≻≻", amark="≻≻").execute()
        return result

    @classmethod
    def get_input(cls, datatype, message, secret):
        if secret:
            data = inquirer.secret(message=message, transformer=lambda _: "[hidden]", style=cls.style, qmark="≻≻",
                                   amark="≻≻").execute()
        else:
            data = inquirer.text(message=message, style=cls.style, qmark="≻≻", amark="≻≻").execute()
        if datatype is str:
            if isinstance(data, str):
                return data
            return str(data)
        return data

    @classmethod
    def get_custom_style(cls):
        return cls.style

    @classmethod
    def get_filepath(cls, message, validate, default=None):
        if default is None:
            default = "~/" if os.name == "posix" else "C:\\"
        if validate == "FILE":
            filepath = inquirer.filepath(message=message, default=default,
                                         validate=PathValidator(is_file=True, message="Input must be a file")).execute()
        elif validate == "DIRECT

ORY":
            filepath = inquirer.filepath(message=message, default=default,
                                         validate=PathValidator(is_file=True, message="Input must be a file")).execute()
        else:
            raise ValidationValueError(f"Validate must be set to 'FILE' or 'DIRECTORY' cannot be: {validate}.")
        return filepath

    @classmethod
    def get_filepath_gui(cls):
        tkinter.Tk().withdraw()
        filepath = filedialog.askopenfilename()
        return filepath

    @classmethod
    def clear_screen(cls):
        clear = lambda: os.system('cls')
        clear()

    @classmethod
    def save_error_prompt(cls):
        answer = askokcancel(title='Error', message='The filepath you selected was not recognised.')
        return answer

    @classmethod
    def display_start_message(cls, message):
        width = Utils.get_terminal_width()
        m = Figlet(font='slant', width=width)
        printy(m.renderText("CommandBlade"), 'o')
        print(message.center(width))

    @classmethod
    def create_menu_list(cls, hooks):
        instruction_data = {}
        choices = [Choice(value='console', name="Console Mode", enabled=True), ]
        end = [Choice(value=None, name="Exit", enabled=True)]
        for hook in hooks:
            choices.append(Choice(value=hook['ID'], name=hook['choice_name'], enabled=True))
            instruction_data[hook['ID']] = hook
        choices.extend(end)
        return choices, instruction_data

    @classmethod
    def get_menu_list(cls):
        hooks = Load.get_hooks()
        choices, instruction_data = cls.create_menu_list(hooks)
        return choices, instruction_data
```

## Creating Plugins

To create a new plugin, follow these steps:

1. Create a new Python file in the `plugins` directory.
2. Define a `Plugin` class with a `process` method and a `get_hook` method.

Example plugin:

```python
class Plugin:
    def process(self):
        print('My Plugin Loaded Successfully')

    @staticmethod
    def get_hook():
        ui_hook = {
            'ID': '01',
            'module': 'my_plugin',
            'class': 'MyPluginClass',
            'method': 'my_plugin_method',
            'choice_name': 'My Plugin'
        }
        return ui_hook
```

3. Implement your plugin's functionality in the specified class and method.

## Running the Application

Run the application using:

```bash
python main.py
```

## Example Plugins

Refer to the `plugins` directory for example plugins, such as:

- `geotrack.py`
- `hash_generator.py`
- `mediocre_crypt.py`
- `password_generator.py`
- `qrcode_generator.py`

These examples demonstrate various functionalities and can serve as a template for creating your own plugins.

---

This documentation should help you get started with CommandBlade and guide you through creating and managing your plugins. If you encounter any issues or have questions, please refer to the example plugins or reach out for support.
