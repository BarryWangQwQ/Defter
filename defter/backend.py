import os
import re
import sys
import eel
import time
import socket
import brython
import warnings
import threading
import subprocess
from contextlib import closing

bv = brython.__version__
IS_WIN32 = 'win32' in str(sys.platform).lower()


def init(path="AppResources", allowed_extensions=None, js_result_timeout=10000, python_in_web=False):
    if allowed_extensions is None:
        allowed_extensions = ['.html']
    else:
        allowed_extensions.insert(0, '.html')
    eel.init(path, allowed_extensions=allowed_extensions, js_result_timeout=js_result_timeout)
    with open('AppResources/core.js', 'w+') as js_core:
        if python_in_web:
            print("Enabled python programming in the web-app page.")
            js_core.write(
                """document.write("<script src='eel.js'></script>","<script src='brython.js'></script>","<script src='brython_stdlib.js'></script>");window.onload=function(){brython();};function expose(f){eel.expose(f);}""")
        else:
            js_core.write(
                """document.write("<script src='eel.js'></script>");function expose(f){eel.expose(f);}""")


def expose(f):
    eel.expose(f)


def start(start_urls="app.html", port="auto", mode='', selfcode=None, **kwargs):
    def get_free_port():
        """ Get free port"""
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

    def subprocess_call(*args, **kwargs):
        # It creates a new *hidden* window, so it will work in frozen apps (.exe).
        if IS_WIN32:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            kwargs['startupinfo'] = startupinfo
        retcode = subprocess.call(*args, **kwargs)
        return retcode

    def electron_run():
        time.sleep(0.1)
        subprocess_call("cd " + os.getcwd() + "/AppResources" + " && npm start", shell=True)

    if selfcode is None:
        with open(os.getcwd() + '/main.py', 'r', encoding='UTF-8') as code:
            codes = code.read()
    else:
        codes = selfcode

    if codes.find(".expose(") != -1:
        warnings.warn('Exposing functions via decorators only is allowed', SyntaxWarning)
        sys.exit(1)

    def subString(w1, w2, template):
        pat = re.compile(w1 + '(.*?)' + w2, re.S)
        return pat.findall(template)

    functions = subString(".expose", ":", codes)
    functions_js = []
    for function in functions:
        functions_js.append("function " + function[function.find("def") + 4:].lstrip() + "{return eel." + function[
                                                                                                          function.find(
                                                                                                              "def") + 4:].lstrip() + ";}")
    with open('AppResources/core.js', 'a+') as code:
        for function_js in functions_js:
            code.write(function_js)

    if port == "auto" or port == 0:
        autoport = get_free_port()
        print("Defter app is running on port", autoport)
        print("Localhost -> http://127.0.0.1:" + str(autoport) + "/app.html" + " or " + "http://localhost:" + str(
            autoport) + "/app.html")
        if mode == "electron":
            '''
            print("Defter app is running as electron...")
            t = threading.Thread(target=electron_run)
            t.start()
            eel.start(start_urls, port=autoport, mode=False, **kwargs)
            '''
            warnings.warn('Electron does not support automatic port assignment!', SyntaxWarning)
            sys.exit(1)
        else:
            eel.start(start_urls, port=autoport, mode=mode, **kwargs)
    else:
        if mode == "electron":
            print("Defter app is running as electron...")
            t = threading.Thread(target=electron_run)
            t.start()
            eel.start(start_urls, mode=False, **kwargs)
        else:
            eel.start(start_urls, mode=mode, **kwargs)


# TODO 上次更新 2021/8/12 15:30
