# -*- coding: utf-8 -*-

"""
Author     : BarryWang
Description: Project Defter App
"""

import sys
from io import open
from setuptools import setup, find_packages

with open('README.md') as read_me:
    long_description = read_me.read()


def platform_requires():
    max_bit = sys.maxsize
    if max_bit > 2 ** 32:
        return ['bottle', 'bottle-websocket', 'future', 'pyparsing', 'whichcraft', 'transcrypt', 'orjson']
    else:
        return ['bottle', 'bottle-websocket', 'future', 'pyparsing', 'whichcraft', 'transcrypt']


setup(
    name='defter',
    version="2.0b2",
    author="BarryWang",
    author_email="StarBarry777@qq.com",
    description="Project Defter App",
    url="https://github.com/BarryWangQwQ/defter",
    packages=find_packages(),
    package_data={
        '': ['*.js', '*.ico', '*.html'],
    },
    install_requires=platform_requires(),
    extras_require={
        "jinja2": ['jinja2>=2.10']
    },
    python_requires='>=3.8',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['defter', 'gui', 'python', 'html', 'javascript', 'electron'],
    entry_points={'console_scripts': [
        'defter = defter.feature.cli:main',
        'defter-frontendc = defter.feature.frontendc:main',
        'defter-packager = defter.backend.__main__:main',
        'defter-accelerator = defter.feature.accelerator:main',
    ]},
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
    ],
)
