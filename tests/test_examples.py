# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from glob import glob

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

mains = []

# have explicit imports here as both __import__ and Popen made issues
try:
    from examples.color_example import main as color_example
    mains += [color_example]
except ImportError:
    print('Ignore example: color_example')

try:
    from examples.custom_ticks_example import main as custom_ticks_example
    mains += [custom_ticks_example]
except ImportError:
    print('Ignore example: custom_ticks_example')

try:
    from examples.ellipse_example import main as ellipse_example
    mains += [ellipse_example]
except ImportError:
    print('Ignore example: ellipse_example')

try:
    from examples.histograms_example import main as histograms_example
    mains += [histograms_example]
except ImportError:
    print('Ignore example: histograms_example')

try:
    from examples.house_example import main as house_example
    mains += [house_example]
except ImportError:
    print('Ignore example: house_example')

try:
    from examples.images_example import main as images_example
    mains += [images_example]
except ImportError:
    print('Ignore example: images_example')

try:
    from examples.markers_and_labels_example import main as markers_and_labels_example
    mains += [markers_and_labels_example]
except ImportError:
    print('Ignore example: markers_and_labels_example')

try:
    from examples.olympic_rings_example import main as olympic_rings_example
    mains += [olympic_rings_example]
except ImportError:
    print('Ignore example: olympic_rings_example')

try:
    from examples.performance_example import main as performance_example
    mains += [performance_example]
except ImportError:
    print('Ignore example: performance_example')

try:
    from examples.plot_example import main as plot_example
    mains += [plot_example]
except ImportError:
    print('Ignore example: plot_example')

try:
    from examples.scatter_cats_example import main as scatter_cats_example
    mains += [scatter_cats_example]
except ImportError:
    print('Ignore example: scatter_cats_example')

try:
    from examples.scatter_example import main as scatter_example
    mains += [scatter_example]
except ImportError:
    print('Ignore example: scatter_example')

try:
    from examples.side_by_side_example import main as side_by_side_example
    mains += [side_by_side_example]
except ImportError:
    print('Ignore example: side_by_side_example')

try:
    from examples.span_example import main as span_example
    mains += [span_example]
except ImportError:
    print('Ignore example: span_example')

try:
    from examples.wetterdienst_example import main as wetterdienst_example
    mains += [wetterdienst_example]
except ImportError:
    print('Ignore example: wetterdienst_example')


@pytest.mark.skipif(not have_numpy, reason='No numpy installed.')
@pytest.mark.skipif(not have_pillow, reason='No pillow installed.')
def test_examples():
    assert len(mains) == len(glob('./examples/*_example.py'))
    for main in mains:
        main()
