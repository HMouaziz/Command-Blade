import io
import tkinter
from tkinter import filedialog
from printy import printy
from core.qr_code_generator.utils import save_error_prompt, get_filetype
from core.utils import get_terminal_width


def save_qr_render(data, render_settings, advanced_mode):
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
            from core.ui.interface import qr_code_generator_ui
            qr_code_generator_ui()
    extension = get_filetype(filepath)[1]
    if extension == '.txt':
        with open(filepath, 'w') as f:
            f.write(data.text())
        printy("QR Code saved successfully.", 'y')
    elif extension == '.svg':
        data.svg(filepath, scale=render_settings['scale'],
                 module_color=render_settings['module_color']['SVG'],
                 background=render_settings['background_color']['SVG'],
                 quiet_zone=render_settings['quiet_zone'])
        buffer = io.BytesIO()
        data.svg(buffer)
        printy("QR Code saved successfully.", 'y')
    elif extension == '.eps':
        data.eps(filepath, scale=render_settings['scale'],
                 module_color=render_settings['module_color']['EPS'],
                 background=render_settings['background_color']['EPS'],
                 quiet_zone=render_settings['quiet_zone'])
        out = io.StringIO()
        data.eps(out)
        printy("QR Code saved successfully.", 'y')
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
        printy("QR Code saved successfully.", 'y')
