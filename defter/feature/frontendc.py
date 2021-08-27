import os
import re
import shutil
import argparse


# Parser options ⬇

def main():
    parser = argparse.ArgumentParser(description='Defter Python Front-End Compiler')
    parser.add_argument(
        "script",
        type=str,
        help="Defter Python front-end script."
    )
    parser.add_argument(
        "res_folder",
        type=str,
        help="Folder including all frontend-resources files including file as frontend, html, css, ico, etc."
    )

    # == Template ===================================================================================
    template = """<!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <script src="defter.js"></script>
    <script type="module" src="{module}"></script>
    </head>
    <body>
    </body>
    </html>
    """

    def clean(filepath):
        del_list = os.listdir(filepath)
        for f in del_list:
            file_path = os.path.join(filepath, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        os.rmdir(filepath)

    args, unknown_args = parser.parse_known_args()
    script = args.script
    parent_path = os.path.dirname(args.script)
    res_folder = args.res_folder
    f_name = (os.path.basename(script)).split('.')[0]
    with open(res_folder + '/' + f_name + '.frontend', 'w+', encoding="UTF-8") as frontend:
        frontend.write(template.format(module=(f_name + '.js')))
    os.system("transcrypt " + script)
    os.rename(parent_path + '/__target__/org.transcrypt.__runtime__.js',
              parent_path + '/__target__/DefterVM.runtime.js')
    with open(parent_path + '/__target__/DefterVM.runtime.js', 'r', encoding="UTF-8") as runtime:
        runtime_code = runtime.read()
        runtime_code = re.sub("//# sourceMappingURL=org.transcrypt.__runtime__.map", "", runtime_code)
    with open(parent_path + '/__target__/DefterVM.runtime.js', 'w', encoding="UTF-8") as runtime:
        runtime.write(runtime_code)
    with open(parent_path + '/__target__/' + f_name + '.js', 'r', encoding="UTF-8") as jsapi:
        jsapi_code = jsapi.read()
        jsapi_code = re.sub("//# sourceMappingURL=" + f_name + ".map", "", jsapi_code)
        jsapi_code = re.sub("org.transcrypt.__runtime__.js", "DefterVM.runtime.js", jsapi_code)
    with open(parent_path + '/__target__/' + f_name + '.js', 'w', encoding="UTF-8") as jsapi:
        jsapi.write(jsapi_code)
    shutil.copyfile(parent_path + '/__target__/' + f_name + '.js', res_folder + '/' + f_name + '.js')
    shutil.copyfile(parent_path + '/__target__/DefterVM.runtime.js', res_folder + '/DefterVM.runtime.js')
    clean(parent_path + '/__target__')
    print('Already compiled.\n')
    print('''
    ''' + script + '''.py -> Compiler -> ''' + res_folder + '''
    |-- ''' + f_name + '''.frontend       (Front-end entry code)
    |-- ''' + f_name + '''.js             (JavaScript API)
    |-- DefterVM.runtime.js       (DefterVM Runtime library)
    ''')
    print('Done.\n')


if __name__ == '__main__':
    main()
