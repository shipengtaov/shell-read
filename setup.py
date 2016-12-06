#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="shell_read",
    version="0.1.0",
    packages=find_packages(),
    summary="read and write post",
    author_email="shispt18@gmail.com",

    install_requires=[
        'configparser',
        'colorama',
        'requests',
    ],

    entry_points={
        'console_scripts': [
            'sread = shell_read:read',
            'swrite = shell_read:write',
        ]
    }
)
