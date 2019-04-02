from lunas import Iterator
from lunas.readers.nested import Enumerate
from lunas.readers.range import Range, Count

d1 = Range(10, )
d2 = Count(3, bufsize=1)
d = Enumerate(d1, 1)
it = Iterator(d, 3, cache_size=1000, sample_size_fn=lambda x: x[0], sort_cache_by=lambda x: -x[0])
outputs = []
for x in it.iter_epoch():
    print(x.data)
    outputs.append(x.data)

for x in sorted(outputs, key=lambda x: x[0][0]):
    print(x)
