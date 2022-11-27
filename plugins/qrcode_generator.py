import io
import os
import subprocess
import tkinter
import pyqrcode
from tkinter import filedialog
from InquirerPy import inquirer
from InquirerPy.base import Choice
from printy import printy
from core.ui.interface import main_menu
from core.ui.utils import get_custom_style, save_error_prompt, clear_screen, get_color_picker
from core.utils import get_settings, get_terminal_width, get_filetype, update_settings, get_menu_list


class Plugin:
    @staticmethod
    def process():
        print('QR Code Generator Plugin Loaded Successfully')

    @staticmethod
    def get_hook():
        """ UFI is Unique Feature Identifier:  1-B-HW = new_feature-beta_level-Hello_World
            [feature type](1= feature addition, 2= modification of existing feature)
            [random number](3 random integers)
            [feature name initials]"""
        ui_hook = {'UFI': '1-910-QRCG', 'module': 'qrcode_generator', 'class': 'QRCodeGenerator',
                   'method': 'qr_code_generator_ui', 'choice_name': 'QR Code Generator'}
        return ui_hook


class QRCodeGenerator:
    style = None

    def __init__(self):
        self.style = get_custom_style()

    @classmethod
    def qr_code_generator_ui(cls):
        settings = get_settings()
        style = cls.style
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
            cls.qr_code_generator_ui()
        elif select == 2:
            cls.qr_code_generator_settings_ui(settings)
        elif select is None:
            choices, instruction_data = get_menu_list()
            print(choices)
            main_menu(choices, instruction_data)

    @classmethod
    def qr_code_generator_settings_ui(cls, settings):
        if settings['qr_s_advanced_mode'] is True:
            advanced_setting = "Disable Advanced Mode"
        else:
            advanced_setting = "Enable Advanced Mode"
        style = cls.style
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
            cls.qr_code_generator_settings_ui(updated_settings)
        elif select == 2:
            cls.qr_code_encoding_settings_ui(settings)
        elif select == 3:
            cls.qr_code_rendering_settings_ui(settings)
        elif select is None:
            cls.qr_code_generator_ui()

    @classmethod
    def qr_code_encoding_settings_ui(cls, settings):
        style = cls.style
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
            cls.qr_code_encoding_settings_ui(updated_settings)
        elif select == 2:
            version = int(inquirer.number(message="Enter Version Size:", max_allowed=40, min_allowed=1, style=style,
                                          qmark="≻≻", amark="≻≻").execute())
            settings['qr_e_version'] = version
            update_settings(settings)
            updated_settings = get_settings()
            cls.qr_code_encoding_settings_ui(updated_settings)
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
            cls.qr_code_encoding_settings_ui(updated_settings)
        elif select == 4:
            printy(f'Correction level:\n'
                   f'Sets the error correction level of the code. Each level has an associated name given by a letter: '
                   f'L, M, Q, or H; each level can correct up to 7, 15, 25, or 30 percent of the data respectively.\n'
                   f'Version size:\n'
                   f'Specifies the size and data capacity of the code. Versions are any integer between 1 and 40. '
                   f'Where version 1 is the smallest QR code, and version 40 is the largest. By default, the object '
                   f'uses the data’s encoding and error correction level to calculate the smallest possible version.\n'
                   f'Encoding mode:\n'
                   f'Sets how the contents will be encoded. By default, the most efficient encoding is used for the '
                   f'contents.\n', 'g')
            back = inquirer.select(message='', choices=[Choice(value=None, name="Back")], style=style, qmark="≻≻",
                                   amark="≻≻", default=None).execute()
            if back is None:
                clear_screen()
                cls.qr_code_encoding_settings_ui(settings)
        elif select is None:
            cls.qr_code_generator_settings_ui(settings)

    @classmethod
    def qr_code_rendering_settings_ui(cls, settings):
        style = cls.style
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
            cls.qr_code_rendering_settings_ui(updated_settings)
        elif select == 2:
            b_color = get_color_picker(settings['qr_r_background_color'])
            settings['qr_r_background_color'] = b_color
            update_settings(settings)
            updated_settings = get_settings()
            cls.qr_code_rendering_settings_ui(updated_settings)
        elif select == 3:
            scale = int(inquirer.number(message="Enter Scale:", min_allowed=1, style=style, qmark="≻≻",
                                        amark="≻≻").execute())
            settings['qr_r_scale'] = scale
            update_settings(settings)
            updated_settings = get_settings()
            cls.qr_code_rendering_settings_ui(updated_settings)
        elif select == 4:
            q_zone = int(inquirer.number(message="Enter Quiet Zone Size:", min_allowed=1, style=style, qmark="≻≻",
                                         amark="≻≻").execute())
            settings['qr_r_quiet_zone'] = q_zone
            update_settings(settings)
            updated_settings = get_settings()
            cls.qr_code_rendering_settings_ui(updated_settings)
        elif select == 5:
            printy(f'QR Color:\n'
                   f'The color of the QR modules.\n'
                   f'Background Color:\n'
                   f'The color of the background of the QR code.\n'
                   f'Scale:\n'
                   f'The size of a single data module in pixels. Setting this parameter to one, will result in each '
                   f'data module taking up 1 pixel. In other words, the QR code would be too small to scan. What scale '
                   f'to use depends on how you plan to use the QR code. Generally, three, four, or five will result in '
                   f'small but scanable QR codes.\n'
                   f'Quiet Zone:\n'
                   f'An empty area around the QR code. The area is the background module in color. '
                   f'According to the standard this area should be four modules wide.', 'g')
            back = inquirer.select(message='', choices=[Choice(value=None, name="Back")], style=style, qmark="≻≻",
                                   amark="≻≻", default=None).execute()
            if back is None:
                clear_screen()
                cls.qr_code_rendering_settings_ui(settings)
        elif select is None:
            cls.qr_code_generator_settings_ui(settings)


def generate_qr_code(request):
    encode_settings = request['encode_settings']
    render_settings = request['render_settings']

    if request['advanced_mode'] is True:
        data = pyqrcode.create(content=request['data'], error=encode_settings['error_correction_level'],
                               version=encode_settings['version'], mode=encode_settings['encoding_mode'])
    else:
        data = pyqrcode.create(request['data'])

    check, filepath = save_qr_render(data, render_settings, request['advanced_mode'])
    if check:
        printy("QR Code saved successfully.", 'y')
        try:
            os.startfile(filepath)
        except AttributeError:
            subprocess.call(['open', filepath])


def save_qr_render(data, render_settings, advanced_mode):
    check = bool
    if advanced_mode is False:
        render_settings = {"quiet_zone": 5,
                           "module_color": {"PNG": [0, 0, 0, 255],
                                            "SVG": " #000",
                                            "EPS": (0, 0, 0)},
                           "background_color": {"PNG": [255, 255, 255, 0],
                                                "SVG": None,
                                                "EPS": None},
                           "scale": 5}
    else:
        pass
    tkinter.Tk().withdraw()
    filepath = ''
    filetypes = [('Text Document', '.txt'), ('Scalable Vector Graphic', '.svg'), ('Encapsulated PostScript', '.eps'),
                 ('Portable Network Graphic', '.png')]
    try:
        filepath = filedialog.asksaveasfilename(defaultextension='.png',
                                                filetypes=filetypes,
                                                confirmoverwrite=True)
    except FileNotFoundError:
        if filepath != '':
            printy('Filepath not recognized!'.center(get_terminal_width()), '<r')
            retry = save_error_prompt()
            if retry:
                save_qr_render(data, render_settings, advanced_mode)
        else:
            QRCodeGenerator.qr_code_generator_ui()
    extension = get_filetype(filepath)[1]
    if extension == '.txt':
        with open(filepath, 'w') as f:
            f.write(data.text())
        check = True
    elif extension == '.svg':
        data.svg(filepath, scale=render_settings['scale'],
                 module_color=render_settings['module_color']['SVG'],
                 background=render_settings['background_color']['SVG'],
                 quiet_zone=render_settings['quiet_zone'])
        buffer = io.BytesIO()
        data.svg(buffer)
        check = True
    elif extension == '.eps':
        if render_settings['module_color']['EPS'] == render_settings['background_color']['EPS']:
            data.eps(filepath, scale=render_settings['scale'],
                     module_color=render_settings['module_color']['EPS'],
                     background=None,
                     quiet_zone=render_settings['quiet_zone'])
        else:
            data.eps(filepath, scale=render_settings['scale'],
                     module_color=render_settings['module_color']['EPS'],
                     background=render_settings['background_color']['EPS'],
                     quiet_zone=render_settings['quiet_zone'])
        out = io.StringIO()
        data.eps(out)
        check = True
    elif extension == '.png':
        with open(filepath, 'wb') as fstream:
            data.png(fstream, scale=render_settings['scale'],
                     module_color=render_settings['module_color']['PNG'],
                     background=render_settings['background_color']['PNG'],
                     quiet_zone=render_settings['quiet_zone'])
        data.png(filepath, scale=render_settings['scale'],
                 module_color=render_settings['module_color']['PNG'],
                 background=render_settings['background_color']['PNG'],
                 quiet_zone=render_settings['quiet_zone'])
        buffer = io.BytesIO()
        data.png(buffer)
        check = True
    return check, filepath
