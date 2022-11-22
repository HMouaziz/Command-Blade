import random
import string

from core.password_generator.utils import update_password_generator_settings


def debugger():
    settings = {"p_type": "Char",
                "length": "10",
                "use_capitals": False,
                "use_digits": True,
                "use_symbols": False
                }
    update_password_generator_settings(settings)


def generate_password(p_type, length, capital, digits, symbols):
    characters = ''
    if capital is True:
        characters = characters.join(string.ascii_letters)
    elif digits is True:
        characters = characters.join(string.digits)
    elif symbols is True:
        characters = characters.join(string.punctuation)
    elif capital is False:
        characters = characters.join(string.ascii_lowercase)
    password = ''.join(random.choice(characters) for _ in range(int(length)))
    return password
