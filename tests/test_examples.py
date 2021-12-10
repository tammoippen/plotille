# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from glob import glob
import os
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


@pytest.fixture
def change_to_examples_dir(request):
    os.chdir(request.fspath.dirname + '/../examples')
    yield
    os.chdir(str(request.config.invocation_dir))


@pytest.mark.skipif(not have_numpy, reason='No numpy installed.')
@pytest.mark.skipif(not have_pillow, reason='No pillow installed.')
def test_examples(change_to_examples_dir):
    sys.path.insert(0, '.')
    if sys.version.startswith('3.'):
        from importlib import reload
    reload(sys)
    sys.setdefaultencoding('UTF8')
    for fname in glob('*_example.py'):
        print(fname)
        name = fname.split('.')[0]
        example_module = __import__(name)
        example_module.main()
