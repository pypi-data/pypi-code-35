import itertools


def chunks(iterable, size=1000):
    """
    Make digestible chunks of something that can be iterated

    Arguments
    ---------
    iterable: list, tuple, generator
        Just have to support the iter function will break it
        in digestible chunks
    size: size of the digestibles chunks

    Examples
    --------
    >>> [ list( chunk ) for chunk in chunks( range( 10 ), size=5 ) ]
    [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]
    """
    iterator = iter( iterable )
    for i in iterator:
        yield itertools.chain( [i], itertools.islice( iterator, size - 1 ) )
