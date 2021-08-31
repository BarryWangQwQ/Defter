import pkg_resources as pkg
import PyInstaller.__main__ as pyi
import os
from argparse import ArgumentParser


def main():
    parser = ArgumentParser(description="""Project Defter App""")
    parser.add_argument(
        "main_script",
        type=str,
        help="Main back-end python file to run app from"
    )
    parser.add_argument(
        "resources_folder",
        type=str,
        help="Folder including all frontend-resources files including file as frontend, html, css, ico, etc."
    )
    args, unknown_args = parser.parse_known_args()
    main_script = args.main_script
    resources_folder = args.resources_folder

    print("Building executable with main script '%s' and web folder '%s'...\n" %
          (main_script, resources_folder))

    defter_js_file = pkg.resource_filename('defter.backend', 'defter.js')
    js_file_arg = '%s%sdefter/backend' % (defter_js_file, os.pathsep)
    web_folder_arg = '%s%s%s' % (resources_folder, os.pathsep, resources_folder)

    needed_args = ['--hidden-import', 'bottle_websocket',
                   '--add-data', js_file_arg, '--add-data', web_folder_arg]
    full_args = [main_script] + needed_args + unknown_args
    print('Running:\npyinstaller', ' '.join(full_args), '\n')

    pyi.run(full_args)


if __name__ == '__main__':
    main()
