import os
import sys
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import EmptyInputValidator
from pyfiglet import Figlet
from printy import printy
from .utils import get_custom_style, get_input, get_filepath, get_settings, update_settings, clear_screen, \
    get_color_picker
from ..console.console import organise_console_input, call_command
from ..hash_checker.operations import hash_string, hash_file
from ..password_generator.operations import generate_password
from ..qr_code_generator.operations import generate_qr_code
from ..utils import get_terminal_width


def start():
    width = get_terminal_width()
    m = Figlet(font='slant', width=width)
    printy(m.renderText("CommandBlade"), 'o')
    print("[  CommandBlade v0.0.3, Halim Mouaziz  ]".center(width))
    main_menu()


def main_menu():
    style = get_custom_style()
    message = "Select Mode:"
    mode = inquirer.select(
        message=message,
        choices=[
            Choice(value=1, name="Console Mode"),
            Choice(value=2, name="Search Engine Mode"),
            Choice(value=3, name="Network Tools Mode"),
            Choice(value=4, name="Hash Checker"),
            Choice(value=5, name="Password Generator"),
            Choice(value=6, name="QR Code Generator"),
            Choice(value=7, name="Settings"),
            Choice(value=None, name="Exit"),
        ],
        default=None,
        style=style,
        qmark="≻≻",
        amark="≻≻"
    ).execute()
    if mode == 1:
        console_ui(start_mode=True)
    elif mode == 2:
        search_engine_ui()
    elif mode == 3:
        network_tools_ui()
    elif mode == 4:
        hash_checker_ui()
    elif mode == 5:
        password_generator_ui()
    elif mode == 6:
        qr_code_generator_ui()
    elif mode == 7:
        settings_ui()
    elif mode is None:
        print("Exiting...")
        sys.exit(1)


def console_ui(start_mode=False):
    if start_mode is True:
        printy("CommandBlade Console Version 0.3.6"
               "\nHalim Mouaziz, Project Hephaestus.", 'o>')
    style = get_custom_style()
    console_input = inquirer.text(message="", style=style, qmark="≻≻", amark="≻≻").execute()
    call_command(input_dict=organise_console_input(console_input))
    console_ui()


def search_engine_ui():
    pass


def network_tools_ui():
    pass


def hash_checker_ui():
    style = get_custom_style()
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
        style=style,
        qmark="≻≻",
        amark="≻≻"
    ).execute()
    if select == 1:
        hash_algorithm = hash_algorithm_selector_ui()
        string_input = get_input(is_string=True, message="Enter string.")
        print(hash_string(hash_algorithm, string_input))
        hash_checker_ui()
    elif select == 2:
        hash_algorithm = hash_algorithm_selector_ui()
        filepath = get_filepath()
        print(filepath)
        hashed_file = hash_file(hash_algorithm, filepath)
        print(hashed_file.hexdigest())
        hash_checker_ui()
    elif select == 3:
        hash_checker_settings_ui()
    elif select is None:
        main_menu()


def hash_checker_settings_ui():
    style = get_custom_style()
    message = ""
    select = inquirer.select(
        message=message,
        choices=[
            Choice(value=1, name="Change hash algorithm"),
            Choice(value=None, name="Exit"),
        ],
        default=None,
        style=style,
        qmark="≻≻",
        amark="≻≻"
    ).execute()
    if select == 1:
        hash_algorithm_selector_ui()
    elif select is None:
        hash_checker_ui()


def hash_algorithm_selector_ui():
    function = inquirer.fuzzy(
        message="Select which hash algorithm you would like to use.",
        choices=[Choice(value="md5", name="MD5"),
                 Choice(value="sha1", name="SHA1"),
                 Choice(value="sha224", name="SHA224"),
                 Choice(value="sha256", name="SHA256"),
                 Choice(value="sha384", name="SHA384"),
                 Choice(value="sha512", name="SHA512"),
                 Choice(value="blake2b", name="BLAKE2B"),
                 Choice(value="blake2s", name="BLAKE2S")
                 ],
        default="",
    ).execute()
    return function


def password_generator_ui():
    style = get_custom_style()
    message = ""
    select = inquirer.select(
        message=message,
        choices=[
            Choice(value=1, name="Generate Password"),
            Choice(value=2, name="Settings"),
            Choice(value=None, name="Exit"),
        ],
        default=None,
        style=style,
        qmark="≻≻",
        amark="≻≻"
    ).execute()
    if select == 1:
        settings = get_settings()
        printy(generate_password(settings['p_type'],
                                 settings['length'],
                                 settings['use_capitals'],
                                 settings['use_digits'],
                                 settings['use_symbols']
                                 ), 'y')
        password_generator_ui()
    elif select == 2:
        password_generator_settings_ui()
    elif select is None:
        main_menu()


def password_generator_settings_ui():
    style = get_custom_style()
    message = ""
    settings = get_settings()
    select = inquirer.select(
        message=message,
        choices=[
            Choice(value=1, name="Change password length"),
            Choice(value=2, name="Change password type"),
            Choice(value=3, name="Select character list"),
            Choice(value=None, name="Exit"),
        ],
        default=None,
        style=style,
        qmark="≻≻",
        amark="≻≻"
    ).execute()
    if select == 1:
        settings['length'] = inquirer.number(
            message="Enter desired password length:",
            validate=EmptyInputValidator(),
        ).execute()
        update_settings(settings)
    elif select == 2:
        settings['p_type'] = inquirer.select(
            message='Select type:',
            choices=[
                Choice(value='Char', name="Characters"),
                Choice(value='Word', name="Words")
            ],
            style=style,
            qmark="≻≻",
            amark="≻≻"
        ).execute()
        update_settings(settings)
    elif select == 3:
        selection = inquirer.checkbox(
            message="Select:",
            choices=[
                Choice(value=1, name="Use capital letters (A-Z)"),
                Choice(value=2, name="Use digits (0-9)"),
                Choice(value=3, name="Use symbols (@!$%&*)")
            ],
            style=style,
            qmark="≻≻",
            amark="≻≻"
        ).execute()
        if 1 in selection:
            settings["use_capitals"] = True
        elif 1 not in selection:
            settings["use_capitals"] = False
        elif 2 in selection:
            settings["use_digits"] = True
        elif 2 not in selection:
            settings["use_digits"] = False
        elif 3 in selection:
            settings["use_symbols"] = True
        elif 3 not in selection:
            settings["use_symbols"] = False
        update_settings(settings)
    elif select is None:
        password_generator_ui()
    password_generator_settings_ui()


def qr_code_generator_ui():
    settings = get_settings()
    style = get_custom_style()
    select = inquirer.select(
        message='',
        choices=[
            Choice(value=1, name="Create QR Code"),
            Choice(value=2, name="Settings"),
            Choice(value=None, name="Exit")
        ],
        style=style,
        qmark="≻≻",
        amark="≻≻",
        default=None
    ).execute()
    if select == 1:
        data = inquirer.text(message='Enter data:', style=style, qmark="≻≻", amark="≻≻",).execute()
        request = {'data': data,
                   'advanced_mode': settings['qr_s_advanced_mode'],
                   'encode_settings': {"error_correction_level": settings['qr_e_error_correction_level'],
                                       "version": settings['qr_e_version'],
                                       "encoding_mode": settings['qr_e_encoding_mode'],
                                       },
                   'render_settings': {"quiet_zone": settings['qr_r_quiet_zone'],
                                       "module_color": settings['qr_r_module_color'],
                                       "background_color": settings['qr_r_background_color'],
                                       "scale": settings['qr_r_scale']}
                   }
        generate_qr_code(request)
        qr_code_generator_ui()
    elif select == 2:
        qr_code_generator_settings_ui(settings)
    elif select is None:
        main_menu()


def qr_code_generator_settings_ui(settings):
    if settings['qr_s_advanced_mode'] is True:
        advanced_setting = "Disable Advanced Mode"
    else:
        advanced_setting = "Enable Advanced Mode"
    style = get_custom_style()
    select = inquirer.select(
        message='',
        choices=[
            Choice(value=1, name=advanced_setting),
            Choice(value=2, name="Encoding Settings"),
            Choice(value=3, name="Rendering Settings"),
            Choice(value=None, name="Exit")
        ],
        style=style,
        qmark="≻≻",
        amark="≻≻",
        default=None
    ).execute()
    if select == 1:
        adv = settings['qr_s_advanced_mode']
        settings['qr_s_advanced_mode'] = not adv
        update_settings(settings)
        updated_settings = get_settings()
        qr_code_generator_settings_ui(updated_settings)
    elif select == 2:
        qr_code_encoding_settings_ui(settings)
    elif select == 3:
        qr_code_rendering_settings_ui(settings)
    elif select is None:
        qr_code_generator_ui()


def qr_code_encoding_settings_ui(settings):
    style = get_custom_style()
    select = inquirer.select(
        message='',
        choices=[
            Choice(value=1, name=f"Change Correction Level from [{settings['qr_e_error_correction_level']}]"),
            Choice(value=2, name=f"Change Version Size from [{settings['qr_e_version']}]"),
            Choice(value=3, name=f"Change Encoding Mode from [{settings['qr_e_encoding_mode']}]"),
            Choice(value=4, name="Settings Information"),
            Choice(value=None, name="Exit")
        ],
        style=style,
        qmark="≻≻",
        amark="≻≻",
        default=None
    ).execute()
    if select == 1:
        c_level = inquirer.select(
            message='Select correction level:',
            choices=[
                Choice(value='H', name="H (Default)"),
                Choice(value='Q', name="Q"),
                Choice(value='M', name="M"),
                Choice(value='L', name="L")
            ],
            style=style,
            qmark="≻≻",
            amark="≻≻",
            default=1
        ).execute()
        settings['qr_e_error_correction_level'] = c_level
        update_settings(settings)
        updated_settings = get_settings()
        qr_code_encoding_settings_ui(updated_settings)
    elif select == 2:
        version = int(inquirer.number(message="Enter Version Size:", max_allowed=40, min_allowed=1, style=style,
                                      qmark="≻≻", amark="≻≻").execute())
        settings['qr_e_version'] = version
        update_settings(settings)
        updated_settings = get_settings()
        qr_code_encoding_settings_ui(updated_settings)
    elif select == 3:
        e_mode = inquirer.select(
            message='Select encoding mode:',
            choices=[
                Choice(value='numeric', name="Numeric"),
                Choice(value='alphanumeric', name="Alphanumeric"),
                Choice(value='kanji', name="Kanji"),
                Choice(value='binary', name="Binary")
            ],
            style=style,
            qmark="≻≻",
            amark="≻≻",
            default=1
        ).execute()
        settings['qr_e_encoding_mode'] = e_mode
        update_settings(settings)
        updated_settings = get_settings()
        qr_code_encoding_settings_ui(updated_settings)
    elif select == 4:
        printy(f'Correction level:\n'
               f'Sets the error correction level of the code. Each level has an associated name given by a letter: '
               f'L, M, Q, or H; each level can correct up to 7, 15, 25, or 30 percent of the data respectively.\n'
               f'Version size:\n'
               f'Specifies the size and data capacity of the code. Versions are any integer between 1 and 40. '
               f'Where version 1 is the smallest QR code, and version 40 is the largest. By default, the object uses '
               f'the data’s encoding and error correction level to calculate the smallest possible version.\n'
               f'Encoding mode:\n'
               f'Sets how the contents will be encoded. By default, the most efficient encoding is used for the '
               f'contents.\n', 'g')
        back = inquirer.select(message='', choices=[Choice(value=None, name="Back")], style=style, qmark="≻≻",
                               amark="≻≻", default=None).execute()
        if back is None:
            clear_screen()
            qr_code_encoding_settings_ui(settings)
    elif select is None:
        qr_code_generator_settings_ui(settings)


def qr_code_rendering_settings_ui(settings):
    style = get_custom_style()
    select = inquirer.select(
        message='',
        choices=[
            Choice(value=1, name=f"Change QR Color from [{settings['qr_r_module_color']}]"),
            Choice(value=2, name=f"Change Background Color from[{settings['qr_r_background_color']}]"),
            Choice(value=3, name=f"Change Scale from [{settings['qr_r_scale']}]"),
            Choice(value=4, name=f"Change Quiet Zone from [{settings['qr_r_quiet_zone']}]"),
            Choice(value=5, name="Settings Information"),
            Choice(value=None, name="Exit")
        ],
        style=style,
        qmark="≻≻",
        amark="≻≻",
        default=None
    ).execute()
    if select == 1:
        n_color = get_color_picker(settings['qr_r_module_color'])
        settings['qr_r_module_color'] = n_color
        update_settings(settings)
        updated_settings = get_settings()
        qr_code_rendering_settings_ui(updated_settings)
    elif select == 2:
        b_color = get_color_picker(settings['qr_r_background_color'])
        settings['qr_r_background_color'] = b_color
        update_settings(settings)
        updated_settings = get_settings()
        qr_code_rendering_settings_ui(updated_settings)
    elif select == 3:
        scale = int(inquirer.number(message="Enter Scale:", min_allowed=1, style=style, qmark="≻≻",
                                    amark="≻≻").execute())
        settings['qr_r_scale'] = scale
        update_settings(settings)
        updated_settings = get_settings()
        qr_code_rendering_settings_ui(updated_settings)
    elif select == 4:
        q_zone = int(inquirer.number(message="Enter Quiet Zone Size:", min_allowed=1, style=style, qmark="≻≻",
                                     amark="≻≻").execute())
        settings['qr_r_quiet_zone'] = q_zone
        update_settings(settings)
        updated_settings = get_settings()
        qr_code_rendering_settings_ui(updated_settings)
    elif select == 5:
        printy(f'QR Color:\n'
               f'The color of the QR modules.\n'
               f'Background Color:\n'
               f'The color of the background of the QR code.\n'
               f'Scale:\n'
               f'The size of a single data module in pixels. Setting this parameter to one, will result in each data '
               f'module taking up 1 pixel. In other words, the QR code would be too small to scan. What scale to use '
               f'depends on how you plan to use the QR code. Generally, three, four, or five will result in small but'
               f' scanable QR codes.\n'
               f'Quiet Zone:\n'
               f'An empty area around the QR code. The area is the background module in color. '
               f'According to the standard this area should be four modules wide.', 'g')
        back = inquirer.select(message='', choices=[Choice(value=None, name="Back")], style=style, qmark="≻≻",
                               amark="≻≻", default=None).execute()
        if back is None:
            clear_screen()
            qr_code_rendering_settings_ui(settings)
    elif select is None:
        qr_code_generator_settings_ui(settings)


def settings_ui():
    pass
