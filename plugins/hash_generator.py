import hashlib
import pyperclip
from InquirerPy import inquirer
from InquirerPy.base import Choice
from core.interface import Interface


class Plugin:
    @staticmethod
    def process():
        print('Hash Generator Plugin Loaded Successfully')

    @staticmethod
    def get_hook():
        ui_hook = {'ID': '01', 'module': 'hash_generator', 'class': 'HashGenerator',
                   'method': 'hash_generator_ui', 'choice_name': 'File Hasher'}
        return ui_hook


class HashGenerator:
    style = Interface.get_custom_style()

    @classmethod
    def hash_generator_ui(cls):
        message = ''
        select = inquirer.select(
            message=message,
            choices=[
                Choice(value=1, name="Hash File"),
                Choice(value=None, name="Exit"),
            ],
            default=None,
            style=cls.style,
            qmark="≻≻",
            amark="≻≻"
        ).execute()
        if select == 1:
            filepath = Interface.get_filepath_gui()
            hash_algorithm = cls.hash_algorithm_selector_ui()
            hashed_file = hash_file(hash_algorithm, filepath)
            h = hashed_file.hexdigest()
            pyperclip.copy(h)
            Interface.print(h, "y")
            cls.hash_generator_ui()
        elif select is None:
            choices, instruction_data = Interface.get_menu_list()
            Interface.main_menu(choices, instruction_data)

    @classmethod
    def hash_algorithm_selector_ui(cls):
        algorithm = inquirer.fuzzy(
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
        return algorithm


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
