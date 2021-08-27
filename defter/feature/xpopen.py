import subprocess
import sys


def Popen(cmd, **kwargs):
    IS_WIN32 = 'win32' in str(sys.platform).lower()
    if IS_WIN32:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(cmd, startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE, shell=True)
        return process
    else:
        return subprocess.Popen(cmd, **kwargs)


def PIPE():
    return subprocess.PIPE


def check_output(param):
    return subprocess.check_output(param)
