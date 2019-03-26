from pkg_resources import DistributionNotFound, iter_entry_points


class AppHooks:
    @classmethod
    def create_train_graph(cls, *args, **kwargs):
        for name, factory in cls._get_factories():
            if name == "train":
                return factory(*args, **kwargs)
        return None

    @classmethod
    def create_serve_graph(cls, *args, **kwargs):
        for name, factory in cls._get_factories():
            if name == "serve":
                return factory(*args, **kwargs)
        return None

    @staticmethod
    def _get_factories():
        for entry_point in iter_entry_points(group="microcosm_sagemaker.app_hooks"):
            try:
                factory = entry_point.load()
                yield entry_point.name, factory
            except DistributionNotFound:
                continue
        yield from []
