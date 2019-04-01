from pathlib import Path

from .modelset import ModelSet


class Manager:
    def __init__(self, model):
        self.model = model

    @property
    def repository(self):
        return self.model.repository

    def all(self, version='HEAD'):
        def select():
            try:
                result = self.repository.git('ls-tree', '--name-only', f'{version}:{self.model.path}')
                return {(key, None): self.get(key=key, version=version)
                        for key in (Path(file).stem for file in result.splitlines())}
            except ValueError:
                return {}

        return ModelSet(self.model, select, version=version)

    def has(self, key, version='HEAD'):
        if isinstance(key, self.model):
            instance = key
            version = key.version or version
        else:
            instance = self.model(_=True, key=key)

        try:
            self.repository.git('cat-file', '-e', f'{version}:{instance.path}')
            return True
        except ValueError:
            return False

    def get(self, key, version='HEAD', load=False, ignore_deleted=False):
        instance = self.model(_=True, key=key)
        if not ignore_deleted and not self.has(instance, version=version):
            raise self.model.DoesNotExist()

        instance.version = self.repository.git('rev-list', '--max-count=1', version, '--', instance.path)
        if load:
            instance.load()

        return instance

    def get_multiple(self, *references):
        def select():
            objects = {}

            for key, version in references:
                reference = self.get(key=key, version=version)
                if (key, reference.version) in objects:
                    objects[(key, version)] = objects[(key, reference.version)]
                else:
                    objects[(key, version)] = reference

            return objects

        return ModelSet(self.model, select)
