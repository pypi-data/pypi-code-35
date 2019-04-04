import random

class LibsvmData(object):
    def __init__(self, filename, label_type, label_map=None):
        # for opening file
        self._dataset_filename = filename
        self._dataset_f = None

        # for storing label mapping
        self._ylabel=None
        if label_map == 'auto':
            self.gen_label_map(filename)
        else:
            self.set_label_map(label_map)
        if label_type == 'float':
            self._map_label = lambda x: float(x)
        elif label_type == 'class':
            if self._ylabel:
                self._map_label = lambda x: self._ylabel[x]
            else:
                raise ValueError("label map not set, you can use 'auto' to auto generate from dataset")
        else:
            raise ValueError('unrecognized label type')

        # for generating CV datasets
        self._cv_seed = 1
        self._cv_folds = 5
        self._cv = []

    def __enter__(self):
        self.open_dataset()
        return self

    def open_dataset(self):
        self._dataset_f = open(self._dataset_filename)

    def __exit__(self, type, value, traceback):
        self._dataset_f.close()

    ### Label Map Functions ####
    def set_label_map(self, label_dict):
        self._ylabel = label_dict

    def get_label_map(self):
        return self._ylabel

    def gen_label_map(self, filename):
        with open(filename) as f:
            y_list = [line.split(None,1)[0] for line in f.readlines()]
        labels = sorted(set(y for y in y_list),key=lambda y:float(y))
        if not self._ylabel:
            self._ylabel = {label:float(i) for i,label in enumerate(labels)}
        if any(label not in self._ylabel for label in labels):
            raise ValueError('unrecognized class {}'.format(label))

    #### dataset operation functions ####
    def read_next(self):
        if not self._dataset_f:
            raise ValueError("dataset not opened, use the 'with LibsvmData(<filename>) as data' statement")
        line = self._dataset_f.readline()
        if line:
            y_i, x_i = line.split(None,1)
            y_i = self._map_label(y_i)
            x_i = {int(feature[0]):float(feature[1]) for feature in (comp.split(':') for comp in x_i.split())}
            return (x_i, y_i)
        else:
            return None
    def reset(self):
        self._dataset_f.seek(0)

    #### cv support
