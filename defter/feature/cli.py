import os
import shutil
import argparse
from defter.feature import demo, new


# Parser options ⬇


def main():
    parser = argparse.ArgumentParser(description='Defter Cli')
    parser.add_argument("-create", type=str)
    parser.add_argument("-demo", type=str)
    args = parser.parse_args()

    if args.create is not None:
        if args.create == "here":
            args.create = os.getcwd()
        if os.path.exists(args.create + '/NewDefterProject'):
            shutil.rmtree(args.create + '/NewDefterProject')
        shutil.copytree(os.path.split(new.__file__)[0], args.create + '/NewDefterProject')
        shutil.rmtree(args.create + '/NewDefterProject/__pycache__')
        shutil.rmtree(args.create + '/NewDefterProject/src/__pycache__')
        os.remove(args.create + '/NewDefterProject/__init__.py')
        os.remove(args.create + '/NewDefterProject/src/__init__.py')

    if args.demo is not None:
        if args.demo == "here":
            args.demo = os.getcwd()

        if os.path.exists(args.demo + '/DemoDefterProject'):
            shutil.rmtree(args.demo + '/DemoDefterProject')
        shutil.copytree(os.path.split(demo.__file__)[0], args.demo + '/DemoDefterProject')
        shutil.rmtree(args.demo + '/DemoDefterProject/__pycache__')
        shutil.rmtree(args.demo + '/DemoDefterProject/src/__pycache__')
        os.remove(args.demo + '/DemoDefterProject/__init__.py')
        os.remove(args.demo + '/DemoDefterProject/src/__init__.py')


if __name__ == '__main__':
    main()
