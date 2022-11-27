import hashlib
from InquirerPy import inquirer
from InquirerPy.base import Choice
from core.ui.interface import main_menu
from core.ui.utils import get_custom_style, get_input, get_filepath
from core.utils import get_menu_list


class Plugin:
    @staticmethod
    def process():
        print('Hash Generator Plugin Loaded Successfully')

    @staticmethod
    def get_hook():
        """ UFI is Unique Feature Identifier:  1-B-HW = new_feature-beta_level-Hello_World
            [feature type](1= feature addition, 2= modification of existing feature)
            [random number](3 random integers)
            [feature name initials]"""
        ui_hook = {'UFI': '1-121-HG', 'module': 'hash_generator', 'class': 'HashGenerator',
                   'method': 'hash_generator_ui', 'choice_name': 'Hash Generator'}
        return ui_hook


class HashGenerator:
    style = get_custom_style()

    @classmethod
    def hash_generator_ui(cls):
        message = "What kind of data type would you like to check?"
        select = inquirer.select(
            message=message,
            choices=[
                Choice(value=1, name="String"),
                Choice(value=2, name="File"),
                Choice(value=3, name="Settings"),
                Choice(value=None, name="Exit"),
            ],
            default=None,
            style=cls.style,
            qmark="≻≻",
            amark="≻≻"
        ).execute()
        if select == 1:
            hash_algorithm = cls.hash_algorithm_selector_ui()
            string_input = get_input(is_string=True, message="Enter string.")
            print(hash_string(hash_algorithm, string_input))
            cls.hash_generator_ui()
        elif select == 2:
            hash_algorithm = cls.hash_algorithm_selector_ui()
            filepath = get_filepath()
            print(filepath)
            hashed_file = hash_file(hash_algorithm, filepath)
            print(hashed_file.hexdigest())
            cls.hash_generator_ui()
        elif select == 3:
            cls.hash_generator_settings_ui()
        elif select is None:
            choices, instruction_data = get_menu_list()
            main_menu(choices, instruction_data)

    @classmethod
    def hash_generator_settings_ui(cls):
        message = ""
        select = inquirer.select(
            message=message,
            choices=[
                Choice(value=1, name="Change hash algorithm"),
                Choice(value=None, name="Exit"),
            ],
            default=None,
            style=cls.style,
            qmark="≻≻",
            amark="≻≻"
        ).execute()
        if select == 1:
            cls.hash_algorithm_selector_ui()
        elif select is None:
            cls.hash_generator_ui()

    @classmethod
    def hash_algorithm_selector_ui(cls):
        function = inquirer.fuzzy(
            message="Select which hash algorithm you would like to use.",
            choices=[Choice(value="md5", name="MD5"),
                     Choice(value="sha1", name="SHA1"),
                     Choice(value="sha224", name="SHA224"),
                     Choice(value="sha256", name="SHA256"),
                     Choice(value="sha384", name="SHA384"),
                     Choice(value="sha512", name="SHA512"),
                     Choice(value="blake2b", name="BLAKE2B"),
                     Choice(value="blake2s", name="BLAKE2S"),
                     ],
            style=cls.style,
            default="",
        ).execute()
        return function


def hash_string(hash_algorithm, input_string):
    if hash_algorithm == "MD5":
        return hashlib.md5(input_string.encode('utf-8')).hexdigest()
    elif hash_algorithm == "SHA1":
        return hashlib.sha1(input_string.encode('utf-8')).hexdigest()
    elif hash_algorithm == "SHA224":
        return hashlib.sha224(input_string.encode('utf-8')).hexdigest()
    elif hash_algorithm == "SHA256":
        return hashlib.sha256(input_string.encode('utf-8')).hexdigest()
    elif hash_algorithm == "SHA384":
        return hashlib.sha384(input_string.encode('utf-8')).hexdigest()
    elif hash_algorithm == "SHA512":
        return hashlib.sha512(input_string.encode('utf-8')).hexdigest()
    elif hash_algorithm == "BLAKE2B":
        return hashlib.blake2b(input_string.encode('utf-8')).hexdigest()
    elif hash_algorithm == "BLAKE2S":
        return hashlib.blake2s(input_string.encode('utf-8')).hexdigest()
    else:
        return "Error"


def hash_file(hash_algorithm, filepath, buffer_size=65536):
    hash_algorithm_function = getattr(hashlib, hash_algorithm.lower())
    file = hash_algorithm_function()
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            file.update(data)
    hashed_file = file
    return hashed_file
