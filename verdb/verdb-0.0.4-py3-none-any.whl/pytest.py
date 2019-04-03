import shutil
from contextlib import ExitStack
from functools import partial
from pathlib import Path
from stat import S_IWRITE
from tempfile import TemporaryDirectory

from pytest import fixture

from verdb.model import Model
from verdb.repository import Repository


@fixture
def verdb():
    def replace_repository(cls):
        if cls.repository:
            original_repositories[cls] = cls.repository

            if cls.repository in replaced_repositories:
                repository = replaced_repositories[cls.repository]
            else:
                repository = Repository(stack.enter_context(TemporaryDirectory()))
                replaced_repositories[cls.repository] = repository

            cls.repository = repository

    original_repositories = {}
    replaced_repositories = {}

    def __init_subclass__(cls, **kwargs):
        original_init_subclass.__func__(cls, **kwargs)
        replace_repository(cls)

    class InitSubclassDescriptor:
        def __get__(self, _, cls):
            return partial(__init_subclass__, cls)

    def subclasses(cls):
        for subclass in cls.__subclasses__():
            yield subclass
            yield from subclasses(subclass)

    def set_writable(_, path, __):
        path = Path(path)
        path.chmod(S_IWRITE)
        path.unlink()

    with ExitStack() as stack:
        original_init_subclass = Model.__init_subclass__
        Model.__init_subclass__ = InitSubclassDescriptor()
        for cls in subclasses(Model):
            replace_repository(cls)

        yield

        Model.__init_subclass__ = original_init_subclass
        for cls, repository in original_repositories.items():
            for item in cls.repository.prefix.iterdir():
                shutil.rmtree(item, onerror=set_writable)
            cls.repository = repository


def pytest_load_initial_conftests(early_config, parser, args):
    early_config.addinivalue_line(
        'markers', 'verdb(): Mark the test as using verdb. '
                   'This will enable database isolation by using an alternate temporary repository.')


@fixture(autouse=True)
def _verdb_marker(request):
    if request.node.get_closest_marker('verdb'):
        request.getfixturevalue('verdb')
