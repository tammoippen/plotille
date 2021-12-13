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


@pytest.mark.skipif(not have_numpy, reason='No numpy installed.')
@pytest.mark.skipif(not have_pillow, reason='No pillow installed.')
def test_examples():
    # have explicit imports here as both __import__ and Popen made issues
    from examples.color_example import main as color_example
    from examples.custom_ticks_example import main as custom_ticks_example
    from examples.ellipse_example import main as ellipse_example
    from examples.histograms_example import main as histograms_example
    from examples.house_example import main as house_example
    from examples.images_example import main as images_example
    from examples.markers_and_labels_example import main as markers_and_labels_example
    from examples.olympic_rings_example import main as olympic_rings_example
    from examples.performance_example import main as performance_example
    from examples.plot_example import main as plot_example
    from examples.scatter_cats_example import main as scatter_cats_example
    from examples.scatter_example import main as scatter_example
    from examples.side_by_side_example import main as side_by_side_example
    from examples.span_example import main as span_example
    from examples.wetterdienst_example import main as wetterdienst_example

    mains = [color_example, custom_ticks_example, ellipse_example, histograms_example,
             house_example, images_example, markers_and_labels_example,
             olympic_rings_example, performance_example, plot_example, scatter_cats_example,
             scatter_example, side_by_side_example, span_example, wetterdienst_example]
    assert len(mains) == len(glob('./examples/*_example.py'))
    for main in mains:
        main()
