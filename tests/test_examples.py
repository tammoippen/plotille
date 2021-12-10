# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from glob import glob
import sys


def test_examples():
    sys.path.insert(0, './examples')
    for fname in glob('examples/*_example.py'):
        name = fname.split('.')[0].split('/')[-1]
        example_module = __import__(name)
        example_module.main()
