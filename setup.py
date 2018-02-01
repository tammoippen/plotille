# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from setuptools import find_packages, setup

try:
    long_description = open('README.rst').read()
except IOError:
    long_description = open('README.md').read()

version = '3.2'

setup(
    name='plotille',
    version=version,
    packages=find_packages(),
    install_requires=[
        'six',
        'pendulum',
    ],
    author='Tammo Ippen',
    author_email='tammo.ippen@posteo.de',
    description='Plot in the terminal using braille dots.',
    long_description=long_description,
    license='MIT',
    url='https://github.com/tammoippen/plotille',
    download_url='https://github.com/tammoippen/plotille/archive/v{}.tar.gz'.format(version),
    keywords=['plot', 'scatter', 'histogram', 'terminal', 'braille', 'unicode', 'timeseries'],
    include_package_data=True,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Terminals'
    ]
)
