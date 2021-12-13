# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from glob import glob
import subprocess
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
    for fname in glob('./examples/*_example.py'):
        p = subprocess.Popen([sys.executable, fname[11:]], cwd='./examples', shell=False,
                             stderr=subprocess.PIPE)
        p.wait()
        assert p.returncode == 0, 'stderr:\n  ' + '  '.join(line.decode('utf-8') for line in p.stderr)
