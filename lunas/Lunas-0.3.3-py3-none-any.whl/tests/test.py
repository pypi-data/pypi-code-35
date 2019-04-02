import random

from lunas import Iterator, TextLine, Zip, Shuffle


def generate():
    with open('src', 'w') as w:
        for i in range(100000):
            w.write(f'{i}.{random.randint(0, 100000)}\n')

    with open('trg', 'w') as w:
        for i in range(100000):
            w.write(f'{i}.{random.randint(0, 100000)}\n')


def clean():
    import os
    os.remove('src')
    os.remove('trg')


def aggregate_value_by_key(dicts, key, reduction=None):
    values = [d[key] for d in dicts]
    if reduction:
        return reduction(values)
    return values


def get_it():
    threads = 6
    src = TextLine('src', num_threads=threads)
    trg = TextLine('trg', num_threads=threads)
    ds = Zip([src, trg], num_threads=threads)

    ds = ds.select(lambda x, y: {
        'xi': int(x.split('.')[0]),
        'yi': int(y.split('.')[0]),
        'x': int(x.split('.')[1]),
        'y': int(y.split('.')[1]),
        'X': x,
        'Y': y,
    })

    shuffle = -1
    if shuffle != 0:
        ds = Shuffle(ds, shufsize=shuffle, num_threads=threads)

    ds = ds.where(
        lambda x: x['x'] % 2 == 0 and x['y'] % 2 == 0
    )

    def collate_fn(xs):
        return {
            'xi': aggregate_value_by_key(xs, 'xi'),
            'yi': aggregate_value_by_key(xs, 'yi'),
            'x': aggregate_value_by_key(xs, 'x'),
            'y': aggregate_value_by_key(xs, 'y'),
            'X': aggregate_value_by_key(xs, 'X'),
            'Y': aggregate_value_by_key(xs, 'Y'),
        }

    sample_size_fn = None

    batch_size = 10

    iterator = Iterator(
        ds, batch_size,
        cache_size=max(20, 1) * batch_size,
        sample_size_fn=sample_size_fn,
        collate_fn=collate_fn,
        sort_cache_by=lambda sample: -sample['y'],
        sort_batch_by=lambda sample: -sample['x'],
        strip_batch=True
    )

    return iterator


def test_align():
    it = get_it()
    for batch in it.iter_epoch():
        assert batch.data['xi'] == batch.data['yi']


def test_filter():
    it = get_it()
    import numpy
    for batch in it.iter_epoch():
        x = numpy.array(batch.data['x'])
        y = numpy.array(batch.data['y'])
        assert numpy.all(x % 2 == 0)
        assert numpy.all(y % 2 == 0)


generate()
test_align()
test_filter()
clean()
