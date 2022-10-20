import subprocess


def ping(args):
    target = 'www.google.com'
    command = ['ping', 'n', '1', target]
    return subprocess.call(command) == 0
