from csv import DictWriter
import json
import torch
import numpy as np
import math
from torch.utils.data import Dataset, DataLoader
from collections import defaultdict


class ColoradoDatasetPostprocessor():
    def __init__(self, spec='competitor_pack/data/colorado-specs.json'):
        with open(spec) as f:
            spec = json.load(f)

        self.num_bits = {}
        for key in spec:
            maxval = spec[key]['maxval']
            self.num_bits[key] = 1 if maxval == 0 else math.ceil(math.log(spec[key]['maxval'] + 1, 2))

    def postprocess(self, f, dump='competitor_pack/postprocessed.csv'):
        tensor = torch.load(f)
        postprocessed = []
        for row in tensor:
            postprocessed_row = {}
            row = row.tolist()
            for i in range(len(row)):
                row[i] = '1' if row[i] > 0.5 else '0'
                    
            start = 0
            for key, bits in sorted(self.num_bits.items()):
                postprocessed_row[key] = int(''.join(row[start:start+bits]), 2)
                start += bits
            
            postprocessed.append(postprocessed_row)

        with open(dump, 'w') as f:
            writer = DictWriter(f, fieldnames=self.num_bits.keys())
            writer.writerow(dict((fn, fn) for fn in writer.fieldnames))
            for row in postprocessed:
                writer.writerow(row)


if __name__ == '__main__':
    postprocessor = ColoradoDatasetPostprocessor()
    postprocessor.postprocess('samples/400.pt')

