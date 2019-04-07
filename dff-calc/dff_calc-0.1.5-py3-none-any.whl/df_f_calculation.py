import numpy as np
import attr
from attr.validators import instance_of
import pandas as pd


@attr.s
class DffCalculator:
    """
    Takes a matrix with rows as independent fluorescent traces,
    and returns a similar-sized matrix with the corresponding dF/F values
    calculated based on https://www.nature.com/articles/nprot.2010.169
    The starting frames might have a 0 dF/F value, due to NaNs being
    converted to 0. This happens following the running window operations
    that are preformed on the data.
    Parameters:
    -----------
        data [np.ndarray]: (cell x time)
        fps [float]: frame rate (Hz)
        tau_0 [float]: exponential smoothing factor in seconds
        tau_1 [float]: F0 smoothing parameter in seconds
        tau_2 [float]: time window before t to minimize
        invert [bool]: False (default) if the transient is expected to be positive, True otherwise
    """

    data = attr.ib(validator=instance_of(np.ndarray))
    fps = attr.ib(default=30.0, validator=instance_of(float))  # Hz
    tau_0 = attr.ib(
        default=0.1, validator=instance_of(float)
    )  # seconds, EWMA parameter
    tau_1 = attr.ib(
        default=0.35, validator=instance_of(float)
    )  # seconds, smoothed F0 parameter
    tau_2 = attr.ib(
        default=2.0, validator=instance_of(float)
    )  # seconds, time window before t to minimize
    invert = attr.ib(default=False, validator=instance_of(bool))
    f0 = attr.ib(init=False)
    unfiltered_dff = attr.ib(init=False)
    dff = attr.ib(init=False)
    trace_num = attr.ib(init=False)  # number of traces
    sample_num = attr.ib(init=False)  # number of samples per trace
    min_per = attr.ib(init=False)

    def calc(self) -> np.ndarray:
        """ Main function to run the calculation
        :returns: Filtered dF/F matrix
        """
        self._calc_f0()
        self._calc_dff_unfiltered()
        self._filter_dff()
        if self.data.ndim == 1:
            return self.dff.to_numpy().ravel()
        else:
            return self.dff.to_numpy().T

    def __attrs_post_init__(self):
        """ Change params to have fitting units """
        self.tau_0 = self.fps * self.tau_0
        self.tau_1 = int(self.fps * self.tau_1)
        self.tau_2 = int(self.fps * self.tau_2)
        self.trace_num = self.data.shape[0]
        self.min_per = max(1, int(self.fps / 10))
        if self.invert:
            self.data = -self.data

    def _calc_f0(self):
        """
        Create the F_0(t) baseline for the dF/F calculation using a boxcar window
        """
        data = pd.DataFrame(self.data.T)
        self.f0 = (
            data.rolling(window=self.tau_1, win_type="boxcar")
            .mean()
            .rolling(window=self.tau_2, min_periods=self.min_per)
            .min()
            + np.finfo(float).eps
        )

    def _calc_dff_unfiltered(self):
        """ Subtract baseline from current fluorescence """
        f0 = self.f0.to_numpy()
        raw_calc = (self.data.T - f0) / f0
        self.unfiltered_dff = pd.DataFrame(raw_calc).fillna(0)

    def _filter_dff(self):
        """ Apply an exponentially weighted moving average to the dF/F data """
        self.dff = (
            self.unfiltered_dff.ewm(halflife=self.tau_0, min_periods=self.min_per)
            .mean()
            .fillna(0)
        )
