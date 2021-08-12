# -*- coding: utf-8 -*-

"""
Author     : BarryWang
Description: Project Defter App
"""

import setuptools


setuptools.setup(
    name='defter',  # 模块名称
    version="1.0b0",  # 当前版本
    author="BarryWang",  # 作者
    author_email="StarBarry777@qq.com",  # 作者邮箱
    description="Project Defter App",  # 模块简介
    url="https://github.com/BarryWangQwQ/defter",  # 模块github地址
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 添加这个选项，在windows下Python目录的scripts下生成exe文件
    # 注意：模块与函数之间是冒号:
    entry_points={'console_scripts': [
        'defter-cli = defter.cli:main',
    ]},
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=['Eel', 'brython'],
    python_requires='>=3.6',
)
