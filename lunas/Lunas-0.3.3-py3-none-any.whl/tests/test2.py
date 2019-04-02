from lunas import Range, Shuffle, Iterator, GroupIterator,Distributed

x = Range(22)
x = Shuffle(x)

import numpy
world=3
for r in range(world):
    print('---',r)
    numpy.random.seed(100)
    y = Distributed(x, world, r)
    it = GroupIterator(Iterator(y, 1), 4)
    for batch in it.iter_epoch():
        print([b.data for b in batch])
        print(len(batch))
    # for b in y:
    #     print(b)
#
# x=list(range(11))
# print(x[9:None:3])