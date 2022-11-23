import os.path
from tkinter.messagebox import askokcancel


def save_error_prompt():
    answer = askokcancel(title='Error', message='The filepath you selected was not recognised.')
    return answer


def get_filetype(filepath):
    filename, filetype = os.path.splitext(filepath)
    split_path = (filename, filetype)
    return split_path
