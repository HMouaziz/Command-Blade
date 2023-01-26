import hashlib
import os.path
from InquirerPy import inquirer
from InquirerPy.base import Choice
from alive_progress import alive_bar
from core.functions import Settings, FileUtil
from core.interface import Interface


class Plugin:
    @staticmethod
    def process():
        print('Mediocre Encrypter Plugin Loaded Successfully')

    @staticmethod
    def get_hook():
        """ UFI is Unique Feature Identifier:  1-B-HW = new_feature-beta_level-Hello_World
            [feature type](1= feature addition, 2= modification of existing feature)
            [random number](3 random integers)
            [feature name initials]"""
        ui_hook = {'UFI': '1-847-ME', 'module': 'mediocre_crypt', 'class': 'MediocreCrypt',
                   'method': 'mediocre_crypt_ui', 'choice_name': 'MediocreCrypt Encryption Tool'}
        return ui_hook


class MediocreCrypt:
    style = Interface.get_custom_style()

    @classmethod
    def mediocre_crypt_ui(cls):
        settings = Settings.get()
        select = inquirer.select(
            message='',
            choices=[
                Choice(value=1, name="Encrypt"),
                Choice(value=2, name="Decrypt"),
                Choice(value=3, name="Settings"),
                Choice(value=None, name="Exit")
            ],
            style=cls.style,
            qmark="≻≻",
            amark="≻≻",
            default=None
        ).execute()
        if select == 1:
            cls.encrypt_file()
            cls.mediocre_crypt_ui()

        elif select == 2:
            cls.decrypt_file()
            cls.mediocre_crypt_ui()

        elif select == 3:
            cls.settings_ui()
            cls.mediocre_crypt_ui()

        elif select is None:
            choices, instruction_data = Interface.get_menu_list()
            Interface.main_menu(choices, instruction_data)

    @classmethod
    def encrypt_file(cls):
        filepath = Interface.get_filepath()
        password = Interface.get_input(message="Enter password:", datatype=str, secret=True)
        ms = MediocreStream(filepath, password)
        ms.encrypt()

    @classmethod
    def decrypt_file(cls):
        filepath = Interface.get_filepath()
        password = Interface.get_input(message="Enter password:", datatype=str, secret=True)
        ms = MediocreStream(filepath, password)
        ms.decrypt()

    @classmethod
    def settings_ui(cls):
        pass


class MediocreStream:
    filepath = str
    password = str
    rw_buffer = 65536

    def __init__(self, filepath, password):
        self.filepath = filepath
        self.password = password
        
    def encrypt(self):
        with alive_bar(4) as bar:
            data = self.get_data()
            bar()
            key_stream = self.get_key_stream()
            bar()
            encrypted_data = self.xor(key_stream=key_stream, data=data)
            bar()
            self.save_data(encrypted_data, encrypt=True)
            bar()

    def decrypt(self):
        with alive_bar(4) as bar:
            data = self.get_data()
            bar()
            key_stream = self.get_key_stream()
            bar()
            decrypted_data = self.xor(key_stream=key_stream, data=data)
            bar()
            self.save_data(decrypted_data, encrypt=False)
            bar()

    def get_data(self):
        data_list = []
        with open(self.filepath, 'rb') as f:
            while True:
                data = f.read(self.rw_buffer)
                if not data:
                    break
                data_list.append(data)
        return b''.join(data_list)

    def save_data(self, data, encrypt=False):
        path, ext = os.path.splitext(self.filepath)
        if encrypt is True:
            extension = '.mc'
            filepath = path + extension
        else:
            filepath = self.filepath

        with open(filepath, 'wb', buffering=self.rw_buffer) as f:
            f.write(data)

        if encrypt is False:
            extension = FileUtil.get_magic_filetype(filepath)
            if extension is None:
                extension = 'txt'
            new_filepath = path + '.' + extension
            os.rename(filepath, new_filepath)

    def get_key_stream(self):
        s = self.initialise_key(self.password)
        return self.generate_key_stream(s)
    
    @classmethod
    def initialise_key(cls, key):
        s = list(range(256))
        j = 0

        key = hashlib.sha256(key.encode('utf-8')).hexdigest()

        key = [ord(c) for c in key]

        for i in range(256):
            j = (j + s[i] + key[i % len(key)]) % 256
            s[i], s[j] = s[j], s[i]
        return s
    
    @classmethod
    def generate_key_stream(cls, s):
        i = 0
        j = 0
        while True:
            i = (i + 1) % 256
            j = (j + s[i]) % 256

            s[i], s[j] = s[j], s[i]
            key_stream = s[(s[i] + s[j]) % 256]
            yield key_stream

    @classmethod
    def xor(cls, key_stream, data: bytes):
        return bytearray([b ^ next(key_stream) for b in bytearray(data)])
