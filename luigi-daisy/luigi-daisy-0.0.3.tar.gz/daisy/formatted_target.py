from luigi import LocalTarget
import copy


def get_formatted_class(ext):
    return _formatted_classes.get(ext, FormattedLocalTargetBase)

_formatted_classes = {}
def _register_ext(ext):
    def _decorator(cls):
        _formatted_classes[ext] = cls
        return cls
    return _decorator

class FormattedLocalTargetBase(LocalTarget):
    def __init__(self, filename, **kwargs):
        self.default_options = kwargs
        super(FormattedLocalTargetBase, self).__init__(filename)

    def load(self, **kwargs):
        opts = {}
        opts.update(self.default_options)
        opts.update(kwargs)

        return self._load(**opts)

    def dump(self, obj, **kwargs):
        opts = {}
        opts.update(self.default_options)
        opts.update(kwargs)

        self.makedirs()
        self._dump(obj, **opts)

    def _load(self, **kwargs):
        raise NotImplementedError()

    def _dump(self, obj, **kwargs):
        raise NotImplementedError()

@_register_ext("csv")
class CsvTarget(FormattedLocalTargetBase):
    def _load(self, **kwargs):
        import pandas as pd
        if "index_col" not in kwargs:
            kwargs["index_col"] = 0

        with self.open('r') as fn:
            return pd.read_csv(fn, **kwargs)

    def _dump(self, obj, **kwargs):
        import pandas as pd

        obj = pd.DataFrame(obj)
        with self.open('w') as fn:
            return obj.to_csv(fn, **kwargs)

@_register_ext("npy")
class NpyTarget(FormattedLocalTargetBase):
    def _load(self, **kwargs):
        import numpy as np
        return np.load(self.path, **kwargs)

    def _dump(self, obj, **kwargs):
        import numpy as np
        np.save(self.path, obj, **kwargs)

@_register_ext("json")
class JsonTarget(FormattedLocalTargetBase):
    def _load(self, **kwargs):
        import json
        with self.open("r") as fn:
            return json.load(fn, **kwargs)

    def _dump(self, obj, **kwargs):
        import json
        with self.open("w") as fn:
            json.dump(obj, fn, **kwargs)

@_register_ext("pkl")
@_register_ext("pickle")
class PickleTarget(FormattedLocalTargetBase):
    def _load(self, **kwargs):
        import pickle

        with open(self.path, "rb") as fn:
            return pickle.load(fn)
        
    def _dump(self, obj, **kwargs):
        import pickle
        with open(self.path, "wb") as fn:
            pickle.dump(obj, fn, **kwargs)

@_register_ext("feather")
class FeatherTarget(FormattedLocalTargetBase):
    def _load(self, **kwargs):
        import pandas as pd
        with self.open('rb') as fn:
            return pd.read_feather(fn, **kwargs)

    def _dump(self, obj, **kwargs):
        import pandas as pd

        obj = pd.DataFrame(obj)
        with self.open('wb') as fn:
            return obj.to_feather(fn, **kwargs)

