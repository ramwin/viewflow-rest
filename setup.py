#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2017-05-24 13:31:49

from setuptools import setup
from codecs import open
from os import path
here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='viewflow-rest',

    version='2.0.1',

    description="viewlflow that support django rest framework",
    long_description=long_description,
    long_description_content_type="text/markdown",

    # The project's main homepage.
    url='https://github.com/ramwin/viewflow-rest',

    # Author details
    author='Xiang Wang',
    author_email='ramwin@qq.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
    ],

    # What does your project relate to?
    keywords='viewflow django-rest-framework viewflow-rest',

    packages=["viewflow_rest"],

    install_requires=['django', 'djangorestframework'],

    data_files=[('README.md', ['README.md'])],
)
