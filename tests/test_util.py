# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from plotille._util import hist

try:
    import numpy as np
    have_numpy = True
except ImportError:
    have_numpy = False


@pytest.mark.skipif(not have_numpy, reason='No numpy installed.')
def test_hist_neg_idx():
    x = np.random.randint(-32767, 32767, 100, dtype=np.int16)

    expect = np.histogram(x, bins=8)
    actual = hist(x, bins=8)

    assert list(expect[0]) == actual[0]  # counts
    assert list(expect[1]) == actual[1]  # bins
