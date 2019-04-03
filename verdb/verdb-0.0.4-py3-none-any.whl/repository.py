import platform
from contextlib import contextmanager
from pathlib import Path
from subprocess import run, CalledProcessError
from tempfile import TemporaryDirectory


def _run(command, **kwargs):
    result = run(command, capture_output=True, **kwargs)

    try:
        result.check_returncode()
        return result.stdout.decode('utf-8').strip()
    except CalledProcessError:
        raise ValueError(result.stderr.decode('utf-8').strip())


class Repository:
    repositories = {}

    def __new__(cls, prefix):
        absolute_prefix = Path(prefix).absolute()
        if absolute_prefix in cls.repositories:
            return cls.repositories[absolute_prefix]
        else:
            repository = super().__new__(cls)
            cls.repositories[absolute_prefix] = repository
            return repository

    def __init__(self, prefix):
        self.prefix = Path(prefix).absolute()
        self._work_tree = None
        self._index = None

    def __repr__(self):
        return f'{type(self).__name__}(prefix="{self.prefix}")'

    def git(self, *args, **kwargs):
        git_dir = Path(self.prefix, '.git')
        if not git_dir.exists():
            _run(['git', 'init', '--bare', str(git_dir)], cwd=self.prefix)

        command = ['git'] + [str(arg) for arg in args if arg]
        env = {
            'GIT_DIR': str(git_dir),
            **{f'GIT_{key.upper()}': str(value) for key, value in kwargs.items() if value},
            **({'GIT_INDEX_FILE': self._index} if self._index else {}),
            **({'GIT_WORK_TREE': self._work_tree} if self._work_tree else {})
        }
        cwd = self._work_tree if self._work_tree else self.prefix
        return _run(command, cwd=cwd, env=env)

    @contextmanager
    def commit(self, message):
        if self._index or self._work_tree:
            yield self._work_tree
            return

        with TemporaryDirectory() as self._index, TemporaryDirectory() as self._work_tree:
            self._index = str(Path(self._index, 'index'))
            self.git('reset')

            yield self._work_tree

            self.git(
                'commit',
                '--allow-empty',
                '--allow-empty-message',
                f'--message={message}',
                author_name='VerDB',
                author_email=f'verdb@{platform.node()}',
                committer_name='VerDB',
                committer_email=f'verdb@{platform.node()}')
            self._index = self._work_tree = None
