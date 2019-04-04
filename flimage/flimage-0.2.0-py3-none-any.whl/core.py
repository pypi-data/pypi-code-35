import pathlib

import h5py
import numpy as np
import qpimage

from .image_data import Fluorescence
from .meta import FLMetaDict, DATA_KEYS, META_KEYS_FL
from ._version import version as __version__


class FLImage(object):
    # required to create in-memory hdf5 files with unique fd
    _instances = 0

    def __init__(self, data=None, meta_data={}, h5file=None, h5mode="a",
                 h5dtype="float32",
                 ):
        """Fluorescence image manipulation

        This class makes available fluorescence microscopy data in a
        manner similar to :class:`qpimage.QPImage`.

        Parameters
        ----------
        data: 2d ndarray (float or complex) or list
            The experimental fluorescence image.
        meta_data: dict
            Meta data associated with the input data.
            see :data:`flimage.meta.META_KEYS`
        h5file: str, pathlib.Path, h5py.Group, h5py.File, or None
            A path to an hdf5 data file where all data is cached. If
            set to `None` (default), all data will be handled in
            memory using the "core" driver of the :mod:`h5py`'s
            :class:`h5py:File` class. If the file does not exist,
            it is created. If the file already exists, it is opened
            with the file mode defined by `hdf5_mode`. If this is
            an instance of h5py.Group or h5py.File, then this will
            be used to internally store all data.
        h5mode: str
            Valid file modes are (only applies if `h5file` is a path)

            - "r": Readonly, file must exist
            - "r+": Read/write, file must exist
            - "w": Create file, truncate if exists
            - "w-" or "x": Create file, fail if exists
            - "a": Read/write if exists, create otherwise (default)

        h5dtype: str
            The datatype in which to store the image data. The default
            is "float32" which is sufficient for 2D image analysis and
            consumes only half the disk space of the numpy default
            "float64".
        """
        if (data is not None and
                not isinstance(data, (np.ndarray, list, tuple))):
            msg = "`data` must be numpy.ndarray!"
            if isinstance(data, (str, pathlib.Path)):
                msg += " Did you mean `h5file={}`?".format(data)
            raise ValueError(msg)
        if isinstance(h5file, h5py.Group):
            self.h5 = h5file
            self._do_h5_cleanup = False
        else:
            if h5file is None:
                h5kwargs = {"name": "flimage{}.h5".format(FLImage._instances),
                            "driver": "core",
                            "backing_store": False,
                            "mode": "a"}
            else:
                h5kwargs = {"name": h5file,
                            "mode": h5mode}
            self.h5 = h5py.File(**h5kwargs)
            self._do_h5_cleanup = True
        FLImage._instances += 1
        # set meta data
        meta = FLMetaDict(meta_data)
        for key in meta:
            self.h5.attrs[key] = meta[key]
        if "qpimage version" not in self.h5.attrs:
            self.h5.attrs["qpimage version"] = qpimage.__version__
        if "flimage version" not in self.h5.attrs:
            self.h5.attrs["flimage version"] = __version__
        # set data
        self._fl = Fluorescence(self.h5.require_group("fluorescence"),
                                h5dtype=h5dtype)
        if data is not None:
            self._fl["raw"] = data
        self.h5dtype = h5dtype

    def __enter__(self):
        return self

    def __eq__(self, other):
        datame = [self.meta[k] for k in self.meta if k in DATA_KEYS]
        dataot = [other.meta[k] for k in other.meta if k in DATA_KEYS]

        if (isinstance(other, FLImage) and
            self.shape == other.shape and
            np.allclose(self.fl, other.fl) and
                datame == dataot):
            return True
        else:
            return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._do_h5_cleanup:
            self.h5.flush()
            self.h5.close()

    def __contains__(self, key):
        return key in self.h5.attrs

    def __getitem__(self, given):
        """Slice FLImage `fl` and return a new FLImage

        The background data of the returned QPImage is merged into
        the "data" background array, i.e. there will be no other
        background array.
        """
        if isinstance(given, (slice, tuple)):
            # return new QPImage
            fli = FLImage(data=self.raw_fl[given],
                          meta_data=self.meta)
            return fli
        elif isinstance(given, str):
            # return meta data
            return self.meta[given]
        else:
            msg = "Only slicing and meta data keys allowed for `__getitem__`"
            raise ValueError(msg)

    def __repr__(self):
        if "identifier" in self:
            ident = self["identifier"]
        else:
            ident = hex(id(self))
        rep = "FLImage <{}>, {x}x{y}px".format(ident,
                                               x=self._fl.raw.shape[0],
                                               y=self._fl.raw.shape[1],
                                               )
        if "wavelength" in self:
            wl = self["wavelength"]
            if wl < 2000e-9 and wl > 10e-9:
                # convenience for light microscopy
                rep += ", λ={:.1f}nm".format(wl * 1e9)
            else:
                rep += ", λ={:.2e}m".format(wl)

        return rep

    def __setitem__(self, key, value):
        if key not in META_KEYS_FL:
            raise KeyError("Unknown meta data key: {}".format(key))
        else:
            self.h5.attrs[key] = value

    @property
    def bg_fl(self):
        """background fluorescence image"""
        return self._fl.bg

    @property
    def fl(self):
        """background-corrected fluorescence image"""
        return self._fl.image

    @property
    def dtype(self):
        """dtype of the fluorescence data array"""
        return self._fl.raw.dtype

    @property
    def info(self):
        """list of tuples with FLImage meta data"""
        info = []
        # meta data
        meta = self.meta
        for key in meta:
            info.append((key, self.meta[key]))
        # background correction
        info += self._fl.info
        return info

    @property
    def meta(self):
        """dictionary with imaging meta data"""
        return FLMetaDict(self.h5.attrs)

    @property
    def raw_fl(self):
        """raw fluorescence image"""
        return self._fl.raw

    @property
    def shape(self):
        """size of image dimensions"""
        return self._fl.h5["raw"].shape

    def copy(self, h5file=None):
        """Create a copy of the current instance

        This is done by recursively copying the underlying hdf5 data.

        Parameters
        ----------
        h5file: str, h5py.File, h5py.Group, or None
            see `FLImage.__init__`
        """
        h5 = qpimage.core.copyh5(self.h5, h5file)
        return FLImage(h5file=h5, h5dtype=self.h5dtype)

    def set_bg_data(self, bg_data):
        """Set background fluorescence data

        Parameters
        ----------
        bg_data: 2d ndarray, FLImage, or `None`
            The background data (must be same type as `data`).
            If set to `None`, the background data is reset.
        """
        if isinstance(bg_data, FLImage):
            fl = bg_data.fl
        elif bg_data is None:
            # Reset phase and amplitude
            fl = None
        else:
            # Compute phase and amplitude from bg_data
            fl = bg_data
        # Set background data
        self._fl.set_bg(fl, key="data")
