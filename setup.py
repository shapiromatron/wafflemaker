#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import re
from setuptools import setup, find_packages


def get_version():
    regex = r"""^__version__ = '(.*)'$"""
    with open('wafflemaker/__init__.py', 'r') as f:
        text = f.read()
    return re.findall(regex, text, re.MULTILINE)[0]


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'matplotlib',
    'pandas',
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
    'pytest-mpl',
]
extras = {
    'test': test_requirements,
}

setup(
    name='wafflemaker',
    version=get_version(),
    description="A python package to generate waffle plots",
    long_description=readme + '\n\n' + history,
    author="Andy Shapiro",
    author_email='shapiromatron@gmail.com',
    url='https://github.com/shapiromatron/wafflemaker',
    packages=find_packages(include=['wafflemaker']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='wafflemaker',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    extras_require=extras,
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
