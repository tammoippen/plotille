# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import math
from random import random

from plotille._normalize import Normalize


def test_random_numbers():
    norm = Normalize(-10, 10)

    for _ in range(1000):
        x = random() * 20 - 10
        norm_x = norm(x)
        assert 0 <= norm(x) <= 1
        assert x == norm_x * 20 - 10


def test_random_array():
    norm = Normalize(-10, 10)

    for _ in range(1000):
        x = [random() * 20 - 10 for _ in range(10)]
        norm_x = norm(x)
        assert len(x) == len(norm_x)
        assert all(0 <= y <= 1 for y in norm_x)
        assert x == [y * 20 - 10 for y in norm_x]


def test_bad_values():
    norm = Normalize(-10, 10)

    assert math.isinf(norm(math.inf))
    assert math.isnan(norm(math.nan))
    assert norm(None) is None


def test_bad_values_clip():
    norm = Normalize(-10, 10, clip=True)

    assert norm(math.inf) == 1.0
    assert norm(math.nan) == 1.0
    # is not a number
    assert norm(None) is None
