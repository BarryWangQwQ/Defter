import os
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
        if os.path.exists(path + '/__init__.acceleration'):
            if os.path.exists(path + '/__init__.default'):
                os.remove(path + '/__init__.default')
                print("Warning: Accelerator cache status has been cleared. Please try again.")
            else:
                if max_bit > 2 ** 32:
                    os.rename(path + '/__init__.py', path + '/__init__.default')
                    os.rename(path + '/__init__.acceleration', path + '/__init__.py')
                    print("Accelerator is enabled.")
                else:
                    print('Error: Failed to enable acceleration. (Your platform may be 32-bit or does not support acceleration.)')
        else:
            print("Accelerator has been enabled.")
    elif boolean == "False":
        if os.path.exists(path + '/__init__.default'):
            if os.path.exists(path + '/__init__.acceleration'):
                os.remove(path + '/__init__.default')
                print("Warning: Accelerator cache status has been cleared. Please try again.")
            else:
                if max_bit > 2 ** 32:
                    os.rename(path + '/__init__.py', path + '/__init__.acceleration')
                    os.rename(path + '/__init__.default', path + '/__init__.py')
                    print("Accelerator is disabled.")
                else:
                    print("Accelerator has been disabled.")
        else:
            print("Accelerator has been disabled.")


if __name__ == '__main__':
    main()
