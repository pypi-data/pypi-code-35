from .main import Interpolator


def interpolate(method, x, y, z, gridsize=25, validation='jacknife',
                src_epsg=25832, tgt_epsg=4326, agg=None, **kwargs):
    if validation is not None:
        kwargs['validation'] = dict(func=validation)

    kwargs['gridsize'] = gridsize

    # build interpolator
    interpolator = dict(
        func=method,
        params=kwargs
    )

    # build settings
    settings = dict(
        agg=agg,
        interpolator=interpolator
    )

    # build Interpolator
    return Interpolator(x, y, z, settings, src_epsg=src_epsg, tgt_epsg=tgt_epsg)
