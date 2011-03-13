#!/usr/bin/env python

from setuptools import setup, find_packages

import os
execfile(os.path.join('kokki', 'version.py'))

setup(
    name = 'kokki',
    version = VERSION,
    description = 'Kokki is a system configuration management framework influenced by Chef',
    author = 'Samuel Stauffer',
    author_email = 'samuel@descolada.com',
    url = 'http://samuelks.com/kokki/',
    packages = find_packages(),
    test_suite = "tests",
    entry_points = {
        "console_scripts": [
            "kokki = kokki.command:main",
        ],
    },
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires = [
        'jinja2',
    ],
)
