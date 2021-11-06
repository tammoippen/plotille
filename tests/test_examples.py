# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from glob import glob
import sys

import pytest

try:
    import numpy  # noqa: F401
    have_numpy = True
except ImportError:
    have_numpy = False


try:
    from PIL import Image  # noqa: F401
    have_pillow = True
except ImportError:
    have_pillow = False


@pytest.mark.skipif(not have_numpy, reason='No numpy installed.')
@pytest.mark.skipif(not have_pillow, reason='No pillow installed.')
def test_examples():
    sys.path.insert(0, './examples')
    for fname in glob('examples/*_example.py'):
        name = fname.split('.')[0].split('/')[-1]
        example_module = __import__(name)
        example_module.main()
