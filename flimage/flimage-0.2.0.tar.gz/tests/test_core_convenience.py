import numpy as np

import flimage


def test_contains():
    fli = flimage.FLImage(data=np.zeros((10, 10)))
    assert "hans-peter" not in fli


def test_equals():
    data = np.zeros((10, 10))
    meta_data = {"pixel size": .14}
    fli = flimage.FLImage(data=data, meta_data=meta_data)

    fli1 = fli.copy()
    assert fli1 == fli

    fli1["pixel size"] = .15
    assert fli1 != fli


def test_repr():
    # make sure no errors when printing repr
    size = 200
    fl = np.repeat(np.linspace(0, np.pi, size), size)
    fl = fl.reshape(size, size)
    fli = flimage.FLImage(fl, meta_data={"pixel size": 0.13})
    print(fli)

    print(fli._fl)


def test_setitem():
    data = np.zeros((10, 10))
    meta_data = {"pixel size": .13e-6}
    fli = flimage.FLImage(data=data, meta_data=meta_data)

    fli["pixel size"] = 0.14e-6

    assert fli["pixel size"] == 0.14e-6

    try:
        fli["unknown.data"] = "42"
    except KeyError:
        pass
    else:
        assert False, "Unknown meta name sould raise KeyError."


if __name__ == "__main__":
    # Run all tests
    loc = locals()
    for key in list(loc.keys()):
        if key.startswith("test_") and hasattr(loc[key], "__call__"):
            loc[key]()
