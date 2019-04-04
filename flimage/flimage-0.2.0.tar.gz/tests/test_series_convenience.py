import pathlib

import numpy as np

import flimage


def test_getitem():
    size = 20
    fl = np.repeat(np.linspace(0, 10, size), size)
    fl = fl.reshape(size, size)

    fli1 = flimage.FLImage(data=1.1 * fl)
    fli2 = flimage.FLImage(data=1.2 * fl)
    fli3 = flimage.FLImage(data=1.3 * fl)

    series = flimage.FLSeries(flimage_list=[fli1, fli2, fli3])

    assert fli1 != fli2
    assert fli1 != fli3
    assert series[0] == fli1
    assert series[1] == fli2
    assert series[2] == fli3
    assert series[-3] == fli1
    assert series[-2] == fli2
    assert series[-1] == fli3

    try:
        series[-4]
    except ValueError:
        pass
    else:
        assert False, "Negative index exceeds size."


def test_getitem_identifier():
    size = 20
    fl = np.repeat(np.linspace(0, 10, size), size)
    fl = fl.reshape(size, size)

    fli1 = flimage.FLImage(data=1.1 * fl,
                           meta_data={"identifier": "peter"})
    fli2 = flimage.FLImage(data=1.2 * fl,
                           meta_data={"identifier": "hans"})
    fli3 = flimage.FLImage(data=1.3 * fl,
                           meta_data={"identifier": "doe"})

    series = flimage.FLSeries(flimage_list=[fli1, fli2, fli3])
    assert "peter" in series
    assert "peter_bad" not in series
    assert series["peter"] == fli1
    assert series["peter"] != fli2
    assert series["hans"] == fli2
    assert series["doe"] == fli3
    try:
        series["john"]
    except KeyError:
        pass
    else:
        assert False, "'john' is not in series"
    try:
        series.add_flimage(fli1)
    except ValueError:
        pass
    else:
        assert False, "Adding FLImage with same identifier should not work"


def test_identifier():
    h5file = pathlib.Path(__file__).parent / "data" / "basic.h5"
    fli = flimage.FLImage(h5file=h5file, h5mode="r")
    series1 = flimage.FLSeries(flimage_list=[fli, fli, fli],
                               identifier="test_identifier")
    assert series1.identifier == "test_identifier"

    series2 = flimage.FLSeries(flimage_list=[fli, fli, fli])
    assert series2.identifier is None


def test_identifier_flimage():
    size = 20
    fl = np.repeat(np.linspace(0, 10, size), size)
    fl = fl.reshape(size, size)

    fli1 = flimage.FLImage(data=1.1 * fl)
    fli2 = flimage.FLImage(data=1.2 * fl)
    fli3 = flimage.FLImage(data=1.3 * fl)

    series = flimage.FLSeries(flimage_list=[fli1, fli2])
    series.add_flimage(fli=fli3, identifier="hastalavista")
    assert series[2]["identifier"] == "hastalavista"


def test_iter():
    h5file = pathlib.Path(__file__).parent / "data" / "basic.h5"
    fli = flimage.FLImage(h5file=h5file, h5mode="r")
    series = flimage.FLSeries(flimage_list=[fli, fli, fli])

    for qpj in series:
        assert qpj == fli


if __name__ == "__main__":
    # Run all tests
    loc = locals()
    for key in list(loc.keys()):
        if key.startswith("test_") and hasattr(loc[key], "__call__"):
            loc[key]()
