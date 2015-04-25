#!/usr/bin/env python

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'CHANGELOG.rst')) as file_changelog:
    changelog = file_changelog.read()

with open(os.path.join(here, 'README.rst')) as file_readme:
    readme = file_readme.read()

long_description = readme + '\n\n' + changelog


setup(
    name='pinion',
    version='0.0.1',
    author='Simeon Visser',
    author_email='simeonvisser@gmail.com',
    description='Gearman client/server',
    long_description=long_description,
    url='https://github.com/svisser/pinion/',
    packages=find_packages(),
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='gearman pinion client server'
)
