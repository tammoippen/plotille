


import pytest

from plotille._cmaps import cmaps
# from plotille._colors import color


@pytest.mark.parametrize('name', cmaps.keys())
def test_print_cmaps(name, tty):
    # print()
    current = cmaps[name]()
    for v in range(1000):
        c = current(v / 1000.0)
        assert len(c) == 3
        assert all(0 <= comp <= 255 for comp in c)
        assert all(int(comp) == comp for comp in c)

        # print(color(' ' * 10, bg=c, mode='rgb'))
