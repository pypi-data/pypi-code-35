import h5py

import lmfit
import numpy as np
from skimage.restoration import denoise_tv_chambolle

from .core import FLImage
from .meta import FLMetaDict


class FLSeries(object):
    _instances = 0

    def __init__(self, flimage_list=[], meta_data={},
                 h5file=None, h5mode="a", identifier=None):
        """Fluorescence microscopy series data

        Parameters
        ----------
        flimage_list: list
            A list of instances of :class:`flimage.FLImage`.
        meta_data: dict
            Meta data associated with the input data
            (see :const:`flimage.META_KEYS`). This overrides
            the meta data of the FLImages in `flimage_list` and, if
            `h5file` is given and `h5mode` is not "r", overrides
            the meta data in `h5file`.
        h5file: str, h5py.Group, h5py.File, or None
            A path to an hdf5 data file where all data is cached. If
            set to `None` (default), all data will be handled in
            memory using the "core" driver of the :mod:`h5py`'s
            :class:`h5py:File` class. If the file does not exist,
            it is created. If the file already exists, it is opened
            with the file mode defined by `hdf5_mode`. If this is
            an instance of h5py.Group or h5py.File, then this will
            be used to internally store all data. If `h5file` is given
            and `flimage_list` is not empty, all FLImages in
            `flimage_list` are appended to `h5file` in the given order.
        h5mode: str
            Valid file modes are (only applies if `h5file` is a path):

            - "r": Readonly, file must exist
            - "r+": Read/write, file must exist
            - "w": Create file, truncate if exists
            - "w-" or "x": Create file, fail if exists
            - "a": Read/write if exists, create otherwise (default)
        """
        if flimage_list and not isinstance(flimage_list, list):
            msg = "`flimage_list` must be a list!"
            if isinstance(flimage_list, str):
                msg += " Did you mean `h5file={}`?".format(flimage_list)
            raise ValueError(msg)
        if isinstance(h5file, h5py.Group):
            self.h5 = h5file
            self._do_h5_cleanup = False
        else:
            if h5file is None:
                h5kwargs = {"name": "flseries{}.h5".format(
                    FLSeries._instances),
                    "driver": "core",
                    "backing_store": False,
                    "mode": "a"}
            else:
                h5kwargs = {"name": h5file,
                            "mode": h5mode}
            self.h5 = h5py.File(**h5kwargs)
            self._do_h5_cleanup = True
        FLSeries._instances += 1

        if meta_data and h5mode == "r":
            msg = "`h5mode` must not be 'r' if `meta_data` is given!"
            raise ValueError(msg)

        # make sure self.h5 is not itself a FLImage file
        if "fluorescence" in self.h5:
            raise ValueError(
                "`h5file` is an FLImage file, not an FLSeries file!")

        # Write QPimage data to h5 file
        for fli in flimage_list:
            self.add_flimage(fli)

        # Update meta data
        if meta_data:
            meta = FLMetaDict(meta_data)
            for ii in range(len(self)):
                flii = self.get_flimage(index=ii)
                for mk in meta:
                    flii.h5.attrs[mk] = meta[mk]

        # Set identifier
        if identifier:
            self.h5.attrs["identifier"] = identifier

    def __contains__(self, flid):
        """test whether an FLImage with the given identifier exists"""
        for ii in range(len(self)):
            fli = self[ii]
            if "identifier" in fli and fli["identifier"] == flid:
                exists = True
                break
        else:
            exists = False
        return exists

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._do_h5_cleanup:
            self.h5.flush()
            self.h5.close()

    def __getitem__(self, index):
        return self.get_flimage(index)

    def __iter__(self):
        for ii in range(len(self)):
            yield self[ii]

    def __len__(self):
        keys = list(self.h5.keys())
        keys = [kk for kk in keys if kk.startswith("fli_")]
        return len(keys)

    @property
    def identifier(self):
        """unique identifier of the series"""
        if "identifier" in self.h5.attrs:
            return self.h5.attrs["identifier"]
        else:
            return None

    def add_flimage(self, fli, identifier=None):
        """Add a FLImage instance to the FLSeries

        Parameters
        ----------
        fli: flimage.FLImage
            The FLImage that is added to the series
        identifier: str
            Identifier key for `fli`
        """
        if not isinstance(fli, FLImage):
            raise ValueError("`fli` must be instance of FLImage!")
        if "identifier" in fli and identifier is None:
            identifier = fli["identifier"]
        if identifier and identifier in self:
            msg = "The identifier '{}' already ".format(identifier) \
                  + "exists! You can either change the identifier of " \
                  + " '{}' or remove it.".format(fli)
            raise ValueError(msg)
        # determine number of flimages
        num = len(self)
        # indices start at zero; do not add 1
        name = "fli_{}".format(num)
        group = self.h5.create_group(name)
        fli.copy(h5file=group)

        if identifier:
            # set identifier
            group.attrs["identifier"] = identifier

    def bleach_correction(self, h5out=None, border_px=20, flscorr=None,
                          count=None, max_count=None):
        """Perform a correction for photobleaching

        Bleaching is modeled with an exponential and an offset.

        Parameters
        ----------
        h5out: path or h5py.Group
            A new FLSeries will be written to this HDF5 file or
            h5py group.
        border_px: int
            Number of border pixels to include for background
            estimation.
        flscorr: FLSeries
            Apply the background correction to this FLSeries
            instead of the current instance. Use this in
            combination with filtered versions of the
            same series.

        Returns
        -------
        bg: float
            Background value subtracted from each image
        flint: 1d ndarray
            Fluorescence intensity trace extracted from the series
        decay: 1d ndarray
            Exponential fit to `flint`
        times: 1d ndarray
            Recording times corresponding to the indices in
            `flint` and `decay`

        Notes
        -----
        It is recommended to first denoise the fluorescence data
        with `FLSeries.denoise` do avoid an amplification of the
        background noise.
        """
        if max_count is not None:
            max_count.value += 3*len(self)
        if flscorr is None:
            flscorr = self
        # get border data
        border = np.ones(self[0].shape, dtype=bool)
        border[border_px:-border_px, border_px:-border_px] = False
        bgavg = np.zeros(len(self))
        for ii, fli in enumerate(self):
            bgavg[ii] = np.mean(fli.fl[border])
            if count is not None:
                count.value += 1
        bg = np.mean(bgavg)
        # intensity values
        flint = np.zeros(len(self))
        for ii, fli in enumerate(self):
            fl = fli.fl - bg
            flint[ii] = np.sum(fl[fl > 0])
            if count is not None:
                count.value += 1
        # time values
        times = np.array([fli["time"] for fli in self])

        # fit exponential
        decay = fit_exponential(times, flint)
        corr = decay[0] / decay

        if h5out:
            # perform bleach correction
            with FLSeries(h5file=h5out) as fls:
                for ii, fli in enumerate(flscorr):
                    fld = (fli.fl - bg) * corr[ii]
                    fln = FLImage(data=fld, meta_data=fli.meta)
                    fls.add_flimage(fln)
                    if count is not None:
                        count.value += 1

        return bg, flint, decay, times

    def denoise(self, h5file, count=None, max_count=None):
        """Denoise fluorescence data

        `h5file` specifies a path or HDF5 group for the FLSeries
        to which the denoised fluorescence data is written."""
        if max_count is not None:
            max_count.value += len(self)
        with FLSeries(h5file=h5file) as fls:
            for fli in self:
                fldn = denoise_tv_chambolle(fli.fl, weight=2)
                fln = FLImage(data=fldn, meta_data=fli.meta)
                fls.add_flimage(fln)
                if count is not None:
                    count.value += 1

    def get_flimage(self, index):
        """Return a single FLImage of the series

        Parameters
        ----------
        index: int or str
            Index or identifier of the FLImage

        Notes
        -----
        Instead of ``fls.get_flimage(index)``, it is possible
        to use the short-hand ``fls[index]``.
        """
        if isinstance(index, str):
            # search for the identifier
            for ii in range(len(self)):
                fli = self[ii]
                if "identifier" in fli and fli["identifier"] == index:
                    group = self.h5["fli_{}".format(ii)]
                    break
            else:
                msg = "FLImage identifier '{}' not found!".format(index)
                raise KeyError(msg)
        else:
            # integer index
            if index < -len(self):
                msg = "Index {} out of bounds for FLSeries of size {}!".format(
                    index, len(self))
                raise ValueError(msg)
            elif index < 0:
                index += len(self)
            name = "fli_{}".format(index)
            if name in self.h5:
                group = self.h5[name]
            else:
                msg = "Index {} not found for FLSeries of length {}".format(
                    index, len(self))
                raise KeyError(msg)
        return FLImage(h5file=group)


def fit_exponential(times, flint):
    def model_fct(params, t):
        ampl = params["amplitude"].value
        decay = params["bleach_decay"].value
        offset = params["offset"].value
        model = ampl*np.exp(-decay*t) + offset
        return model

    def residual(params, t, data):
        return model_fct(params, t)-data

    params = lmfit.Parameters()
    params.add("amplitude",
               value=flint.max()-flint.min(),
               min=flint.min(),
               max=2*flint.max())
    dt = times[-1] - times[0]
    df = flint[-1] - flint[0]
    params.add("bleach_decay",
               value=-dt/df*flint[0]/20,
               min=0,
               brute_step=dt/20)
    params.add("offset",
               value=flint.min(),
               min=0)
    out = lmfit.minimize(residual, params, args=(times, flint))

    model = model_fct(out.params, times)

    return model
