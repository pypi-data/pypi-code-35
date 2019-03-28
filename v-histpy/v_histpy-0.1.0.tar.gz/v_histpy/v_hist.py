#!/usr/bin/env python3

import os
from typing import List
from random import randint

class Histogram(object):

    def __init__(self):
        self.labels: List[str] = []
        self.values: List[str] = []
        self.label_len: int = 1

    def add(self, label: str, value: int):
        self.labels.append(label)
        self.values.append(value)

        if len(label) > self.label_len:
            self.label_len = len(label)

    def show(self):
        max_value = max(self.values)
        rows, columns = os.popen('stty size', 'r').read().split()
        width = int(columns) - (self.label_len + 2)
        dw = max_value / width

        for l, v in zip(self.labels, self.values):
            print("{label:{fill}>{width}}|".format(label=l, fill=' ', width=self.label_len), end='')

            for x in range(width):
                if v > dw * x:
                    print("#", end='')
                else:
                    break;

            print()

    def draw(self, values: List[int]):
        for i, value in enumerate(values):
            self.add(f"{i}", value)

        self.show()
    

def main():
   h = Histogram()
   
   h.draw([randint(0, 3000) for x in range(200)])

if __name__ == '__main__':
    main()
