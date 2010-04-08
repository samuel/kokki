#!/usr/bin/env python

from setuptools import setup, find_packages

from kokki import __version__ as version

setup(
    name = 'kokki',
    version = version,
    description = 'Kokki is a system configuration management framework influenced by Chef',
    author = 'Samuel Stauffer',
    author_email = 'samuel@descolada.com',
    url = 'http://samuelks.com/kokki/',
    packages = find_packages(),
    scripts = ['bin/kokki'],
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
