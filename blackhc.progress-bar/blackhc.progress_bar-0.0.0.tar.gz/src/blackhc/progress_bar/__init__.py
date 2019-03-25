from blackhc.progress_bar.details import TQDMProgressBar, LogFriendlyProgressBar
import sys

use_tqdm = True

if sys.stdout.isatty():
    use_tqdm = False


def create_progress_bar(length, tqdm_args=None):
    if use_tqdm:
        return TQDMProgressBar(length, tqdm_args)
    else:
        return LogFriendlyProgressBar(length)


# TODO(blackhc): detect Jupyter notebooks/Ipython as use TQDM
class ProgressBarIterable:
    def __init__(
        self, iterable, length=None, length_unit=None, unit_scale=None, tqdm_args=None
    ):
        self.iterable = iterable
        self.tqdm_args = tqdm_args

        self.length = length
        if length is not None:
            self.length_unit = length_unit
        else:
            if length_unit is not None:
                raise AssertionError(
                    "Cannot specify length_unit without custom length!"
                )
            self.length_unit = 1

        self.unit_scale = unit_scale or 1

    def __iter__(self):
        if self.length is not None:
            length = self.length
        else:
            try:
                length = len(self.iterable)
            except (TypeError, AttributeError):
                raise NotImplementedError("Need a total number of iterations!")

        progress_bar = create_progress_bar(length * self.unit_scale, self.tqdm_args)
        progress_bar.start()
        for item in self.iterable:
            yield item
            progress_bar.update(self.length_unit * self.unit_scale)
        progress_bar.finish()


def with_progress_bar(
    iterable, length=None, length_unit=None, unit_scale=None, tqdm_args=None
):
    return ProgressBarIterable(
        iterable,
        length=length,
        length_unit=length_unit,
        unit_scale=unit_scale,
        tqdm_args=tqdm_args,
    )
