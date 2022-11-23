import pyqrcode
from core.qr_code_generator.functions import save_qr_render
from core.ui.utils import get_settings


def debugger():
    settings = get_settings()
    data = "https://www.project-hephaestus.com"
    '''request = {'data': data,
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
    generate_qr_code(request)'''


def generate_qr_code(request):
    encode_settings = request['encode_settings']
    render_settings = request['render_settings']

    if request['advanced_mode'] is True:
        data = pyqrcode.create(content=request['data'], error=encode_settings['error_correction_level'],
                               version=encode_settings['version'], mode=encode_settings['encoding_mode'])
    else:
        data = pyqrcode.create(request['data'])

    save_qr_render(data, render_settings, request['advanced_mode'])
