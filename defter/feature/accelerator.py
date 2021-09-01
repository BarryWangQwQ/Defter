import os
import re
import sys
import argparse
from defter import backend


def main():
    parser = argparse.ArgumentParser(description='Defter Python Front-End Compiler')
    parser.add_argument(
        "boolean",
        type=str,
        help="Status of the accelerator (True/False)."
    )

    args, unknown_args = parser.parse_known_args()
    path = os.path.split(backend.__file__)[0]
    boolean = args.boolean

    max_bit = sys.maxsize

    if boolean == "True":
        if max_bit > 2 ** 32:
            with open(path + '/__init__.py', 'r', encoding="UTF-8") as init_py:
                init_py_code = init_py.read()
                if init_py_code.find('import orjson as jsn') == -1:
                    init_py_code = re.sub("import json as jsn", "import orjson as jsn", init_py_code)
                    init_py_code = re.sub('jsn.dumps\(obj, default=lambda o: None\)',
                                          'str(jsn.dumps(obj, default=lambda o: None), encoding="utf-8")', init_py_code)
            with open(path + '/__init__.py', 'w+', encoding="UTF-8") as init_py:
                init_py.write(init_py_code)
            print("Accelerator is activated.")
        else:
            print('Error: Failed to activate acceleration. (Your platform may be 32-bit or does not support acceleration.)')
    elif boolean == "False":
        if max_bit > 2 ** 32:
            with open(path + '/__init__.py', 'r', encoding="UTF-8") as init_py:
                init_py_code = init_py.read()
                if init_py_code.find('import json as jsn') == -1:
                    init_py_code = re.sub("import orjson as jsn", "import json as jsn", init_py_code)
                    init_py_code = re.sub('str\(jsn.dumps\(obj, default=lambda o: None\), encoding="utf-8"\)',
                                          'jsn.dumps(obj, default=lambda o: None)', init_py_code)
            with open(path + '/__init__.py', 'w+', encoding="UTF-8") as init_py:
                init_py.write(init_py_code)
            print("Accelerator is deactivated.")
        else:
            print('Error: Failed to deactivate acceleration. (Your platform may be 32-bit or does not support acceleration.)')
    else:
        print('Wrong parameters!')


if __name__ == '__main__':
    main()
