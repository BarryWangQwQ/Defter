import os
import re
import sys
import shutil
import argparse
from defter.feature import xpopen


# Parser options ⬇

def main():
    parser = argparse.ArgumentParser(description='Defter Python Front-End Compiler')
    parser.add_argument(
        "script",
        type=str,
        help="Defter Python front-end script."
    )
    parser.add_argument(
        "src_folder",
        type=str,
        help="Folder including all frontend-resources files including file as html, css, ico, etc."
    )

    # == Template ===================================================================================
    template = """<!DOCTYPE html>
<html>
  
  <head>
    <meta charset="utf-8">
    <script src="defter.js"></script>
    <script type="module" src="./build/{module}.js"></script>
  </head>
  
  <body>
  </body>

</html>"""

    def delete_last_line(path):
        ori = open(path, 'rb+')
        read_lines = ori.readlines()
        ori.seek(-len(read_lines[-1]), os.SEEK_END)
        ori.truncate()
        ori.close()

    args, unknown_args = parser.parse_known_args()
    script = args.script
    src_folder = args.src_folder
    if os.path.exists(os.getcwd() + '/' + src_folder):
        src_folder_abs = os.getcwd() + '/' + src_folder
    else:
        src_folder_abs = src_folder

    if os.path.exists(src_folder_abs + '/build'):
        operation = input('Warning: build directory already exists, recompile and overwrite? (y/n) ')
        if operation == 'Y' or operation == 'y':
            shutil.rmtree(src_folder_abs + '/build')
        elif operation == 'N' or operation == 'n':
            print('Cancel Compile.')
            sys.exit(0)

    f_name = (os.path.basename(script)).split('.')[0]

    with open(src_folder_abs + '/' + f_name + '.html', 'w+', encoding="UTF-8") as frontend:
        frontend.write(template.format(module=f_name))

    console = xpopen.Popen("cd " + os.getcwd() + " && transcrypt " + script + ' -od ' + src_folder + '/build',
                           shell=True, stdout=xpopen.PIPE, stderr=xpopen.PIPE)
    console_result = []
    lines = 0
    for line in console.stdout.readlines():
        if lines > 2:
            console_result.append(line.decode())
        lines += 1
    for line in console_result:
        print(line)

    if console_result[-2].find('Ready') == -1:
        print('Compile failure.\n')
        pass
    else:
        if os.path.exists(src_folder_abs + '/build/DefterVM.runtime.js'):
            os.remove(src_folder_abs + '/build/DefterVM.runtime.js')
        else:
            os.rename(src_folder_abs + '/build/org.transcrypt.__runtime__.js',
                      src_folder_abs + '/build/DefterVM.runtime.js')

        api_list = [os.path.join(src_folder_abs + '/build', i) for i in os.listdir(src_folder_abs + '/build') if
                    i.endswith('.js')]
        for api in api_list:
            delete_last_line(api)
            with open(api, 'r', encoding="UTF-8") as jsapi:
                jsapi_code = jsapi.read()
                jsapi_code = re.sub("org.transcrypt.__runtime__", "DefterVM.runtime", jsapi_code)
            with open(api, 'w', encoding="UTF-8") as jsapi:
                jsapi.write(jsapi_code)
        print('Compile complete.\n')


if __name__ == '__main__':
    main()
