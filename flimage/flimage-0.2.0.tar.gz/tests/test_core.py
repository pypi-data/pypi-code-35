import numpy as np

import flimage


def test_get_fl():
    # make sure no errors when printing repr
    size = 50
    fl = np.repeat(np.linspace(0, 10, size), size)
    fl = fl.reshape(size, size)

    fli1 = flimage.FLImage(fl)

    # test flses
    assert np.allclose(fli1.fl, fl)


def test_get_amp_fl_nan():
    # make sure no errors when printing repr
    size = 50
    fl = np.repeat(np.linspace(0, 10, size), size)
    fl = fl.reshape(size, size)
    flnan = fl.copy()
    flnan[:4] = np.nan
    fli = flimage.FLImage(flnan)
    assert np.allclose(fli.fl, flnan, equal_nan=True)


def test_slice():
    size = 50
    fl = np.repeat(np.linspace(0, 10, size), size)
    fl = fl.reshape(size, size)

    fli = flimage.FLImage(fl)

    x = 25
    y = 10
    x_size = 25
    y_size = 5
    flic = fli[x:x + x_size, y:y + y_size]
    # simple sanity checks
    assert flic.shape == (x_size, y_size)
    # check bg_correction
    assert np.allclose(flic.fl, fl[x:x + x_size, y:y + y_size])

    # slice along x
    flic2 = fli[x:x + x_size]
    assert flic2.shape == (25, size)
    assert np.allclose(flic2.fl, fl[x:x + x_size])

    # index should not work
    try:
        fli[0]
    except ValueError:
        pass
    else:
        assert False, "simple indexing not supported"


if __name__ == "__main__":
    # Run all tests
    loc = locals()
    for key in list(loc.keys()):
        if key.startswith("test_") and hasattr(loc[key], "__call__"):
            loc[key]()
