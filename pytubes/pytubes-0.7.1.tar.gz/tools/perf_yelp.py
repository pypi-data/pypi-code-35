import time
import sys
import os
from os import path
import tubes
import gzip
import json

FILES = [path.expanduser("~/Downloads/yelp_user.csv")]

def tubes_ver():
    x = (tubes.Each(FILES)
        .read_files()
        .split(b'\n')
        .tsv(headers=False, sep=',')
        .multi(lambda x: tuple(x.get(i, '') for i in range(10)))
        .skip_unless(lambda x: x.slot(9).equals('"None"'))
        .first(100)
    )
    return list(x)

def main():
    print(tubes_ver())


if __name__ == '__main__':
    main()