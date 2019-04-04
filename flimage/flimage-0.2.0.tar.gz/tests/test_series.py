import os
import pathlib
import tempfile

import h5py

import flimage


def test_series_error_file_is_flimage():
    h5file = pathlib.Path(__file__).parent / "data" / "basic.h5"
    fli1 = flimage.FLImage(h5file=h5file, h5mode="r")
    tf = tempfile.mktemp(suffix=".h5", prefix="flimage_test_")
    with fli1.copy(h5file=tf):
        pass

    try:
        flimage.FLSeries(flimage_list=[fli1], h5file=tf)
    except ValueError:
        pass
    else:
        assert False, "tf is a flimage file"
    # cleanup
    try:
        os.remove(tf)
    except OSError:
        pass


def test_series_error_key():
    h5file = pathlib.Path(__file__).parent / "data" / "basic.h5"
    fli1 = flimage.FLImage(h5file=h5file, h5mode="r")
    fli2 = fli1.copy()

    fls = flimage.FLSeries(flimage_list=[fli1, fli2])
    try:
        fls.get_flimage(2)
    except KeyError:
        pass
    else:
        assert False, "get index 2 when length is 2"


def test_series_error_meta():
    h5file = pathlib.Path(__file__).parent / "data" / "basic.h5"
    fli1 = flimage.FLImage(h5file=h5file, h5mode="r")
    fli2 = fli1.copy()

    tf = tempfile.mktemp(suffix=".h5", prefix="flimage_test_")
    with flimage.FLSeries(flimage_list=[fli1, fli2],
                          h5file=tf,
                          h5mode="a"
                          ):
        pass

    try:
        flimage.FLSeries(h5file=tf, h5mode="r",
                         meta_data={"wavelength": 550e-9})
    except ValueError:
        pass
    else:
        assert False, "`meta_data` and `h5mode=='r'`"
    # cleanup
    try:
        os.remove(tf)
    except OSError:
        pass


def test_series_error_noflimage():
    try:
        flimage.FLSeries(flimage_list=["hans", 1])
    except ValueError:
        pass
    else:
        assert False, "flimage list must contain FLImages"


def test_series_from_h5file():
    h5file = pathlib.Path(__file__).parent / "data" / "basic.h5"
    fli1 = flimage.FLImage(h5file=h5file, h5mode="r")
    fli2 = fli1.copy()

    tf = tempfile.mktemp(suffix=".h5", prefix="flimage_test_")
    with flimage.FLSeries(flimage_list=[fli1, fli2],
                          h5file=tf,
                          h5mode="a"
                          ):
        pass

    fls2 = flimage.FLSeries(h5file=tf, h5mode="r")
    assert len(fls2) == 2
    assert fls2.get_flimage(0) == fli1
    # cleanup
    try:
        os.remove(tf)
    except OSError:
        pass


def test_series_from_list():
    h5file = pathlib.Path(__file__).parent / "data" / "basic.h5"
    fli1 = flimage.FLImage(h5file=h5file, h5mode="r")
    fli2 = fli1.copy()

    fls = flimage.FLSeries(flimage_list=[fli1, fli2])
    assert len(fls) == 2
    assert fls.get_flimage(0) == fls.get_flimage(1)


def test_series_h5file():
    tf = tempfile.mktemp(suffix=".h5", prefix="flimage_test_")
    with h5py.File(tf, mode="a") as fd:
        fls = flimage.FLSeries(h5file=fd)
        assert len(fls) == 0
    # cleanup
    try:
        os.remove(tf)
    except OSError:
        pass


def test_series_meta():
    h5file = pathlib.Path(__file__).parent / "data" / "basic.h5"
    try:
        flimage.FLImage(h5file=h5file,
                        meta_data={"pixel size": 0.054e-6},
                        h5mode="r")
    except OSError:
        # no write intent on file
        pass
    else:
        assert False, "should not be able to write"

    fli0 = flimage.FLImage(h5file=h5file, h5mode="r")

    tf = tempfile.mktemp(suffix=".h5", prefix="flimage_test_")
    tf = pathlib.Path(tf)
    with fli0.copy(h5file=tf):
        pass

    fli1 = flimage.FLImage(h5file=tf,
                           meta_data={"pixel size": 0.0554e-6})

    assert fli1.meta["pixel size"] == 0.0554e-6
    qps = flimage.FLSeries(flimage_list=[fli1], meta_data={
                           "pixel size": 0.05574e-6})
    assert qps.get_flimage(0).meta["pixel size"] == 0.05574e-6

    # cleanup
    try:
        tf.unlink()
    except OSError:
        pass


if __name__ == "__main__":
    # Run all tests
    loc = locals()
    for key in list(loc.keys()):
        if key.startswith("test_") and hasattr(loc[key], "__call__"):
            loc[key]()
